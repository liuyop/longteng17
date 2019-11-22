import pytest
import pytest_check as ck
import json


@pytest.mark.nondestructive
@pytest.mark.p1
@pytest.mark.api
def test_bingFuelCard_normal(api, db, case_data):
    """绑定加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_name = case_data.get('user_name')
    id_number = case_data.get('id_number')
    user_id = case_data.get('user_id')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
    else:
        db.add_card(card_number)

    #接口访问
    json_data = {"dataSourceId": data_source_id, "methodId": "01A", "CardUser": {"userName": user_name, "idType": "1", "idNumber": id_number}, "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(5010, res_dict.get("code"))
    ck.equal("绑定成功", res_dict.get("msg"))
    ck.is_true(res_dict.get('success'))
    # 数据库断言
    ck.is_true(db.check_bindcard(card_number, user_id))


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_bind3Card(api, db, case_data):
    """绑定超过2张加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_numbers = case_data.get('card_numbers')
    user_name = case_data.get('user_name')
    id_number = case_data.get('id_number')
    user_id = case_data.get('user_id')

    # 数据准备
    for i in card_numbers:
        db.add_card(i)
        if db.check_card_total(user_id) <= 1:
            db.bind_card(i, user_id)
        else:
            break

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "01A",
                 "CardUser": {
                     "userName": user_name,
                     "idType": "1",
                     "idNumber": id_number
                 },
                 "CardInfo": {
                     "cardNumber": case_data.get('card_numbers')[2]
                 }
    }
    res_dict = api.post(url, json=json_data).json()
    # 响应断言
    ck.equal(5014, res_dict.get("code"))
    ck.equal("每个用户只能绑定两张卡", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))

    # 环境清理
    for i in card_numbers:
        db.del_card(i)


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_blacklistCard(api, db, case_data):
    """绑定黑名单加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_name = case_data.get('user_name')
    id_number = case_data.get('id_number')
    card_status = case_data.get('card_status')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
    else:
        db.add_card(card_number)
    db.set_card_status(card_number, card_status)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "01A",
        "CardUser": {
            "userName": user_name,
            "idType": "1",
            "idNumber": id_number
        },
        "CardInfo": {
            "cardNumber": card_number
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(5011, res_dict.get("code"))
    ck.equal("卡号是否黑名单,无法绑定", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))

    #环境清理
    db.del_card(card_number)


# if __name__ == '__main__':
#     pytest.main(["test_bind_fuel_card.py"])
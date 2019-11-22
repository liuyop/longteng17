import pytest
import pytest_check as ck


@pytest.mark.nondestructive
@pytest.mark.p1
@pytest.mark.api
def test_addFuelCard_normal(api, db, case_data):
    """正常添加加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')

    # 环境检查
    if db.check_card(card_number):
        pytest.skip(f'卡号: {card_number} 已存在')
        # print(f'卡号: {card_number} 已存在')
        # db.del_card(card_number)

    json_data = {"dataSourceId": data_source_id, "methodId": "00A",
                 "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("添加卡成功", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
    # 数据库断言
    ck.is_true(db.check_card(card_number))

    # 环境清理
    # db.del_card(card_number)


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_dataSourceId_noAuthority(api, db, case_data):
    """第三方机构无权限"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
        db.del_card(card_number)

    json_data = {"dataSourceId": data_source_id, "methodId": "00A",
                 "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(100, res_dict.get("code"))
    ck.equal("对不起,您的第三方机构无权限访问该接口", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
    # 数据库断言
    ck.is_false(db.check_card(card_number))


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_methodId_invalid(api, db, case_data):
    """业务Id不存在"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
        db.del_card(card_number)

    json_data = {"dataSourceId": data_source_id, "methodId": "05A",
                 "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(199, res_dict.get("code"))
    ck.equal("业务ID无效", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
    # 数据库断言
    ck.is_false(db.check_card(card_number))


# if __name__ == '__main__':
#     pytest.main(['test_add_fuel_card.py'])
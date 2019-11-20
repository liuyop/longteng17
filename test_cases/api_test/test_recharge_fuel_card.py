import pytest
import pytest_check as ck


@pytest.mark.skip
@pytest.mark.p1
@pytest.mark.api
def test_normalRecharge(api, db, case_data):
    """充值加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    cardBalance = case_data.get('card_balance')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
    else:
        db.add_card(card_number)

    #充值前卡余额
    balance = db.check_cardBalance(card_number)
    print("充值前卡余额:", balance)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "03A",
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("充值成功", res_dict.get("msg"))
    ck.is_true(res_dict.get('success'))
    # 数据库断言（充值后余额)
    ck.equal(balance+cardBalance, db.check_cardBalance(card_number))


@pytest.mark.skip
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_cancelCardRecharge(api, db, case_data):
    """注销加油卡充值"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    cardBalance = case_data.get('card_balance')
    card_status = case_data.get('card_status')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
    else:
        db.add_card(card_number)
    db.set_card_status(card_number, card_status)

    #充值前卡余额
    balance = db.check_cardBalance(card_number)
    print("充值前卡余额:", balance)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "03A",
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(5012, res_dict.get("code"))
    ck.equal("卡号已经注销,无法充值", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))

    # 数据清理
    db.del_card(card_number)


@pytest.mark.skip
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_noCardRecharge(api, db, case_data):
    """卡不存在，充值"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    cardBalance = case_data.get('card_balance')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
        db.del_card(card_number)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "03A",
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(5013, res_dict.get("code"))
    ck.equal("加油卡号不存在", res_dict.get("msg"))
    ck.is_false(res_dict.get("success"))
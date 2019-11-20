import pytest
import pytest_check as ck


@pytest.mark.skip
@pytest.mark.p1
@pytest.mark.api
def test_normalConsumption(api, db, case_data):
    """加油卡消费"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')
    cardBalance = case_data.get('card_balance')

    # 环境检查
    balance = db.check_cardBalance(card_number)
    if balance < cardBalance:
        balance = db.check_cardBalance(card_number, cardBalance)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "04A",
        "CardUser": {
            "userId": user_id
        },
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("消费成功!", res_dict.get("msg"))
    ck.is_true(res_dict.get('success'))

    # 数据库断言（消费后余额)
    ck.equal(balance-cardBalance, db.check_cardBalance(card_number))


@pytest.mark.skip
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_InsufficientBalance(api, db, case_data):
    """加油卡消费,余额不足"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')
    cardBalance = case_data.get('card_balance')

    # 环境检查
    balance = db.check_cardBalance(card_number)
    if balance > cardBalance:
        balance = db.set_cardBalance(card_number, cardBalance)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "04A",
        "CardUser": {
            "userId": user_id
        },
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("对不起，您的余额不足，请充值!", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))


@pytest.mark.skip
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_noCardConsumption(api, db, case_data):
    """加油卡号不存在"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')
    cardBalance = case_data.get('card_balance')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
        db.del_card(card_number)

    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "04A",
        "CardUser": {
            "userId": user_id
        },
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(5013, res_dict.get("code"))
    ck.equal("根据用户ID没有查询到卡号!", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
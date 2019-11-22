import pytest
import pytest_check as ck


@pytest.mark.nondestructive
@pytest.mark.p1
@pytest.mark.api
def test_newUesrScenarios(api, db, case_data):
    """新业务流用例"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')
    user_name = case_data.get('user_name')
    id_number = case_data.get('id_number')
    cardBalance = case_data.get('card_balance')

    #添加加油卡
    add_data = {"dataSourceId": data_source_id, "methodId": "00A",
                 "CardInfo": {"cardNumber": card_number}}
    add_dict = api.post(url, json=add_data).json()
    ck.equal(200, add_dict.get("code"))
    ck.equal("添加卡成功", add_dict.get("msg"))
    ck.is_false(add_dict.get('success'))
    ck.is_true(db.check_card(card_number))

    #绑定加油卡
    bind_data = {
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
    bind_dict = api.post(url, json=bind_data).json()
    ck.equal(5010, bind_dict.get("code"))
    ck.equal("绑定成功", bind_dict.get("msg"))
    ck.is_true(bind_dict.get('success'))
    ck.is_true(db.check_bindcard(card_number, user_id))

    #加油卡充值
    balance = db.check_cardBalance(card_number)
    recharge_data = {
        "dataSourceId": data_source_id,
        "methodId": "03A",
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": cardBalance
        }
    }
    recharge_dict = api.post(url, json=recharge_data).json()
    ck.equal(200, recharge_dict.get("code"))
    ck.equal("充值成功", recharge_dict.get("msg"))
    ck.is_true(recharge_dict.get('success'))
    ck.equal(balance + cardBalance, db.check_cardBalance(card_number))

    #加油卡消费
    balance = db.check_cardBalance(card_number)
    cons_data = {
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
    cons_dict = api.post(url, json=cons_data).json()
    ck.equal(200, cons_dict.get("code"))
    ck.equal("消费成功!", cons_dict.get("msg"))
    ck.is_true(cons_dict.get('success'))
    ck.equal(balance - cardBalance, db.check_cardBalance(card_number))

    #查询加油卡
    params = {
        "dataSourceId": data_source_id,
        "methodId": "02A",
        "userId": user_id,
        "cardNumber": card_number
    }
    search_dict = api.get(url, params=params).json()
    ck.equal(200, search_dict.get("code"))
    ck.equal("成功返回", search_dict.get("msg"))
    ck.is_true(search_dict.get('success'))
    assert len(search_dict["result"]["consumptionDetails"]) >= 1
    assert len(search_dict["result"]["rechargeDetails"]) >= 1

    #数据清理
    db.del_card(card_number)
    db.del_consumptiondetails(card_number)
    db.del_rechargedetails(card_number)
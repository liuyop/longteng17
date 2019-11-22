import pytest
import pytest_check as ck


@pytest.mark.nondestructive
@pytest.mark.p1
@pytest.mark.api
def test_searchRecord(api, db, case_data):
    """加油卡有消费,充值记录"""
    url = '/gasStation/process?'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')

    # 环境检查
    con = db.check_consumptiondetails(card_number)
    rec = db.check_rechargedetails(card_number)
    print(f'{card_number}存在{rec}条充值记录和{con}条消费记录')

    params = {
        "dataSourceId": data_source_id,
        "methodId": "02A",
        "userId": user_id,
        "cardNumber": card_number
    }
    res_dict = api.get(url, params=params).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("成功返回", res_dict.get("msg"))
    ck.is_true(res_dict.get('success'))
    assert len(res_dict["result"]["consumptionDetails"]) >= 1
    assert len(res_dict["result"]["rechargeDetails"]) >= 1


@pytest.mark.nondestructive
@pytest.mark.p1
@pytest.mark.api
def test_searchNoRecord(api, db, case_data):
    """加油卡无消费,充值记录"""
    url = '/gasStation/process?'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')

    # 环境检查
    con = db.check_consumptiondetails(card_number)
    rec = db.check_rechargedetails(card_number)
    print(f'{card_number}存在{rec}条充值记录和{con}条消费记录')
    if con >= 0 or rec >= 0:
        db.del_consumptiondetails(card_number)
        db.del_rechargedetails(card_number)

    params = {
        "dataSourceId": data_source_id,
        "methodId": "02A",
        "userId": user_id,
        "cardNumber": card_number
    }
    res_dict = api.get(url, params=params).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("成功返回", res_dict.get("msg"))
    ck.is_true(res_dict.get('success'))
    assert len(res_dict["result"]["consumptionDetails"]) == 0
    assert len(res_dict["result"]["rechargeDetails"]) == 0


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_searchNoCard(api, db, case_data):
    """加油卡不存在"""
    url = '/gasStation/process?'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')

    # 环境检查
    if db.check_card(card_number):
        print(f'卡号: {card_number} 已存在')
        db.del_card(card_number)

    params = {
        "dataSourceId": data_source_id,
        "methodId": "02A",
        "userId": user_id,
        "cardNumber": card_number
    }
    res_dict = api.get(url, params=params).json()

    # 响应断言
    ck.equal(400, res_dict.get("code"))
    ck.equal("无查询信息", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))


@pytest.mark.nondestructive
@pytest.mark.p2
@pytest.mark.api
@pytest.mark.negative
def test_searchNoUser(api, db, case_data):
    """用户不存在"""
    url = '/gasStation/process?'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')
    user_id = case_data.get('user_id')

    # 环境检查
    if db.check_user(user_id):
        print(f'用户: {user_id} 已存在')
        db.del_user(user_id)

    params = {
        "dataSourceId": data_source_id,
        "methodId": "02A",
        "userId": user_id,
        "cardNumber": card_number
    }
    res_dict = api.get(url, params=params).json()

    # 响应断言
    ck.equal(400, res_dict.get("code"))
    ck.equal("无查询信息", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
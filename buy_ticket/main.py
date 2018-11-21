from buy_ticket import GetTicket

if __name__ == '__main__':
    buyticket = GetTicket()
    # buyticket.test_have_ticket() # 仅测试是否有票
    buyticket.get_ticket()  # 先测试，后购买

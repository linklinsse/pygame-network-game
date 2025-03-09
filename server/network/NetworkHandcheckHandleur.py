class NetworkHandcheckHandleur:

    def is_handcheck_valid(self, data, addr) -> tuple[bool, str]:
        ret_bool = False
        ret_msg = None
        if ("pass" in data):
            ret_bool = True
            ret_msg = "ok;" + str(addr[1]) + ";"
        return ret_bool, ret_msg
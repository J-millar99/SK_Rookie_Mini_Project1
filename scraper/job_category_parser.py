def select_occ1_id(soup):
    occ1_li_tag_list = soup.select("ul#occ1_div li")
    occ1_id_dict = dict()
    for occ1_li_tag in occ1_li_tag_list:
        button_tag = occ1_li_tag.find("button")
        if button_tag:
            occ1_id = button_tag.get("data-item-val")
        span_tag = occ1_li_tag.find("span")
        if occ1_id:
            occ1_id_dict[occ1_id] = span_tag.text
    return occ1_id_dict

def select_occ2_id(soup, id_list):
    occ2_id_dict = dict()
    for id in id_list:
        ul_id = "occ2_ul_" + id
        occ2_li_tag_list = soup.select("ul#" + ul_id + " li")

        for occ2_li_tag in occ2_li_tag_list:
            button_tag = occ2_li_tag.find("button")
            if button_tag:
                occ2_id = tuple(button_tag.get("data-item-val").split("_")) # tuple(occ1_id, occ2_id)
            span_tag = occ2_li_tag.find("span")
            if len(occ2_id) == 2:
                occ2_id_dict[occ2_id[1]] = (occ2_id[0], span_tag.text)
    return occ2_id_dict
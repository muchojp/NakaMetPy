# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import pandas as pd
import re

def parse_bufrtab(file_path: str) -> list:
    with open(file_path, mode="r") as f:
        raw_text = f.readlines()[1:-1]
    # 特定の文字列から始まる行を除く
    _records = list(filter(lambda x: not x.startswith("Table"), raw_text))
    _records = list(filter(lambda x: not x.startswith("#"), _records))
    _records = list(filter(lambda x: not x.startswith("END"), _records))
    # 改行文字削除
    _records = [_record.strip("\n") for _record in _records]
    _records = [_record.strip() for _record in _records]
    # 改行文字のみ
    valid_records = list(filter(lambda x: x != "", _records))
    return valid_records

def parse_tableB_into_dataframe(version: str="STD_0_42") -> pd.DataFrame:
    columns = ["F-XX-YYY", "SCALE", "REFERENCE_VALUE", "BIT_WIDTH", "UNIT", "MNEMONIC", "DESC_CODE", "ELEMENT_NAME"]
    
    bufrtab = f"./tables/bufrtab.TableB_{version:02}"
    valid_records = parse_bufrtab(bufrtab)
    # print(valid_records[-1])
    df = pd.DataFrame([re.split("[|;]", irecord.strip()) for irecord in valid_records])
    # 不要な文字を削除を削除
    df = df.apply(lambda x: x.str.strip())
    # Noneのみの列を削除
    df = df.iloc[:, :-1]
    df.columns = columns
    return df

def parse_tableD_into_dict(version: str="STD_0_42") -> list:
    bufrtab = f"./tables/bufrtab.TableD_{version:02}"
    valid_records = parse_bufrtab(bufrtab)
    data = dict()
    fxxyyy = r"^\d-\d{2}-\d{3}" # F-XX-YYY
    fxxyyy_notlast = r"^\d-\d{2}-\d{3} >" # F-XX-YYY >
    for irecord in valid_records:
        irec_list = [x.strip() for x in re.split("[|;]", irecord.strip())]
        # 1レコードで比較
        if re.match(fxxyyy, irecord):
            ielm_list = []
            iseq_list = irec_list
        else:
            jelm_list = irec_list
            # 2列目のF-XX-YYYで比較
            if re.match(fxxyyy_notlast, jelm_list[1]):
                # " >"を削除
                jelm_list[1] = jelm_list[1][:-2]
                ielm_list.append(dict(FXXYYY=jelm_list[1], NAME=jelm_list[2]))
            else:
                ielm_list.append(dict(FXXYYY=jelm_list[1], NAME=jelm_list[2]))
                data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], DCOD=iseq_list[2], NAME=iseq_list[3], SEQUENCE=ielm_list)
    return data

def parse_codeFlag_into_dict(version: str="STD_0_42") -> list:
    bufrtab = f"./tables/bufrtab.CodeFlag_{version:02}"
    valid_records = parse_bufrtab(bufrtab)
    data = dict()
    fxxyyy = r"^\d-\d{2}-\d{3}" # F-XX-YYY
    valBit_notlast = r"^\d+ >" # \d+ >
    for irecord in valid_records:
        irec_list = [x.strip() for x in re.split("[|;]", irecord.strip())]
        # 1レコードで比較
        if re.match(fxxyyy, irecord):
            ielm_list = []
            dependency = None
            iseq_list = irec_list
        else:
            jelm_list = irec_list
            # 2列目にDependencyがあるかを確認
            if "=" in jelm_list[1]:
                # "f-x1-yy1,f-x2-yy2=1,22,33"
                dependency = jelm_list[1]
            elif re.match(valBit_notlast, jelm_list[1]):
                # " >"を削除
                jelm_list[1] = jelm_list[1][:-2]
                if dependency is None:
                    ielm_list.append(dict(VALBIT=jelm_list[1], MEANING=jelm_list[2]))
                else:
                    ielm_list.append(dict(DEPENDENCY=dependency, VALBIT=jelm_list[1], MEANING=jelm_list[2]))
            else:
                if dependency is None:
                    ielm_list.append(dict(VALBIT=jelm_list[1], MEANING=jelm_list[2]))
                    data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], CODEFLAG=iseq_list[2], HAS_DEPENDENCY=False, VALBITS=ielm_list)
                else:
                    ielm_list.append(dict(DEPENDENCY=dependency, VALBIT=jelm_list[1], MEANING=jelm_list[2]))
                    data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], CODEFLAG=iseq_list[2], HAS_DEPENDENCY=True, DEPENDENCY=dependency, VALBITS=ielm_list)
    # print(data["0-01-034"])
    return data


if __name__=='__main__':
    # df_b = parse_tableB_into_dataframe()
    # print(df_b.tail())
    # dict_d = parse_tableD_into_dict()
    # print(dict_d["3-40-026"])
    # dict_codeFlag = parse_codeFlag_into_dict()
    # print(dict_codeFlag["0-01-033"])
    # print(dict_codeFlag["0-01-034"])
    dict_codeFlag = parse_codeFlag_into_dict("LOC_0_7_1")
    print(dict_codeFlag)
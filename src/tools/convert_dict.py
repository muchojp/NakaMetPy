import re  # Regular expressions library

import re  # Regular expressions library

# def parse_html_table(html_table):
#     """Parses an HTML table string into a Python dictionary."""

#     # Extract table data using regular expressions
#     pattern = r'<tr.*?>(.*?)</tr>'  # Match table rows
#     rows = re.findall(pattern, html_table, re.DOTALL)

#     data_dict = {}
#     for row in rows:
#         # Extract table cells using regular expressions
#         pattern = r'<td.*?>(.*?)</td>'
#         cells = re.findall(pattern, row, re.DOTALL)

#         # Convert cells to dictionary entry
#         code = cells[0].strip()  # First cell is code
#         description = cells[1].strip()  # Second cell is description
#         unit = cells[2].strip()  # Third cell is unit
#         scale = int(cells[3].strip())  # Fourth cell is scale
#         reference_value = int(cells[4].strip())  # Fifth cell is reference value
#         data_width = int(cells[5].strip())  # Sixth cell is data width
#         mnemonic = cells[6].strip()  # Seventh cell is mnemonic

#         if unit == '<a href="CodeFlag_0_STDv31_LOC7.html#013039">Code table</a>':
#             unit = 'Code table'

#         data_dict[code] = {
#             "element_name": description,
#             "unit": unit,
#             "scale": scale,
#             "reference_value": reference_value,
#             "data_width": data_width,
#             "mnemonic": mnemonic
#         }

#     return data_dict
def parse_html_table(html_table):
    """Parses an HTML table string into a Python dictionary."""

    # Extract table data using regular expressions
    pattern = r'<tr.*?>(.*?)</tr>'  # Match table rows
    rows = re.findall(pattern, html_table, re.DOTALL)

    data_dict = {}
    for row in rows:
        # Extract table cells using regular expressions
        pattern = r'<td.*?>(.*?)</td>'
        cells = re.findall(pattern, row, re.DOTALL)

        # Convert cells to dictionary entry
        code = cells[0].strip()  # First cell is code
        description = cells[1].strip()  # Second cell is description
        unit = cells[2].strip()  # Third cell is unit

        # Extract only text content from unit cell if it contains a link
        if unit.startswith('<a href'):
            unit_match = re.search(r">(.*?)</a>", unit)  # Find text within link tags
            if unit_match:
                unit = unit_match.group(1).strip()  # Extract text content

        scale = int(cells[3].strip())  # Fourth cell is scale
        reference_value = int(cells[4].strip())  # Fifth cell is reference value
        data_width = int(cells[5].strip())  # Sixth cell is data width
        mnemonic = cells[6].strip()  # Seventh cell is mnemonic

        data_dict[code] = {
            "element_name": description,
            "unit": unit,
            "scale": scale,
            "reference_value": reference_value,
            "data_width": data_width,
            "mnemonic": mnemonic
        }

    return data_dict

html_table = """
  <tr class="local">
    <td>0-63-000</td>
    <td>Byte count</td>
    <td>Numeric</td>
    <td class="right">0</td>
    <td class="right">0</td>
    <td class="right">16</td>
    <td>BYTCNT</td>
  </tr>
  <tr class="local">
    <td>0-63-255</td>
    <td>Fill bit</td>
    <td>Numeric</td>
    <td class="right">0</td>
    <td class="right">0</td>
    <td class="right">1</td>
    <td>BITPAD</td>
  </tr>
"""


data_dict = parse_html_table(html_table)
for ikey in data_dict.keys():
  print(f'"{ikey}": ' + str(data_dict[ikey]) + ",")
# print(data_dict)

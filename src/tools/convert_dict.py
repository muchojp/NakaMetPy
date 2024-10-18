import re  # Regular expressions library
from bs4 import BeautifulSoup
from pprint import pprint

def parse_html_table_b_x_entries(html_table):
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


def parse_html_table_d_x(html_table):
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
        f = cells[0].strip()  # First cell is code
        x = cells[1].strip()  # Second cell is description
        category = cells[2].strip()  # Third cell is unit

        # Extract only text content from unit cell if it contains a link
        if x.startswith('<a href'):
            x = re.search(r">(.*?)</a>", x)  # Find text within link tags
            if x:
                x = int(x.group(1).strip())  # Extract text content
        if category.startswith('<a href'):
            category = re.search(r">(.*?)</a>", category)  # Find text within link tags
            if category:
                category = category.group(1).strip()  # Extract text content

        data_dict[x] = category

    return data_dict


def parse_html_table_d_x_entries(html):
  """Parses the HTML and returns a dictionary with extracted data.

  Args:
      html: The HTML string to be parsed.

  Returns:
      A dictionary containing key-value pairs extracted from the tables.
  """
  soup = BeautifulSoup(html, 'html.parser')
  result = {}
  
  for table in soup.find_all('table', rules='groups'):
    key = table.find('th').text.strip()  # Get the key from the first th
    data = []
    for row in table.find_all('tr')[1:]:
      value = row.find_all('td')[1].text.strip()  # Get value from the second td
      if not re.search(r'\?-??-\???', value):  # Check if it contains ?-??-???
        data.append(value)
    result[key] = data

  return result

def parse_html_table_code_figure(html):
    # # BeautifulSoupを使ってHTMLをパース
    # soup = BeautifulSoup(html, 'lxml')

    # # SAID情報を含む辞書を作成
    # said_info = {}

    # # table要素を取得
    # tables = soup.find_all('table')

    # # table要素（テーブル）をループ
    # for table in tables:
    #     # tableのIDを取得
    #     table_id = table.get('id')

    #     # SAID情報を含む辞書を作成
    #     said_info_per_table = {}

    #     # tr要素（行）をループ
    #     for tr in table.find_all('tr'):
    #         # 最初のtr要素はヘッダーなのでスキップ
    #         if tr.find('th'):
    #             continue

    #         # td要素（セル）を取得
    #         tds = tr.find_all('td')

    #         # Code figure列の値を取得
    #         code_figure_text = tds[0].text.strip()

    #         # Code figureが数字範囲の場合
    #         if '-' in code_figure_text:
    #             start, end = code_figure_text.split('-')
    #             for code_figure in range(int(start), int(end) + 1):
    #                 said_info_per_table[code_figure] = tds[1].text.strip()
    #         # Code figureが単一数字の場合
    #         else:
    #             code_figure = int(code_figure_text)
    #             said_info_per_table[code_figure] = tds[1].text.strip()

    #     # table IDとSAID情報をsaid_info辞書に追加
    #     said_info[table_id] = said_info_per_table

    # return said_info
    # BeautifulSoupを使ってHTMLをパース
    # BeautifulSoupを使ってHTMLをパース
    soup = BeautifulSoup(html, 'lxml')

    # SAID情報を含む辞書を作成
    said_info = {}

    # table要素（テーブル）をループ
    for table in soup.find_all('table'):
        # table IDを取得
        table_id_match = re.match(r'<h4>(.*?)-.*?</h4>', table.parent.text)  # 親要素からh4タグを取得
        print(table.parent.text)
        if table_id_match:
            table_id = table_id_match.group(1)
        else:
            table_id = f'table_{soup.find_all("table").index(table)}'  # IDが見つからない場合はインデックスを使用

        # SAID情報を含む辞書を作成
        said_info_per_table = {}

        # tr要素（行）をループ
        for tr in table.find_all('tr'):
            # 最初のtr要素はヘッダーなのでスキップ
            if tr.find('th'):
                continue

            # td要素（セル）を取得
            tds = tr.find_all('td')

            # Code Number列の値を取得
            code_figure_text = tds[0].text.strip()

            # Code Numberが数字の場合
            if code_figure_text.isdigit():
                code_figure = int(code_figure_text)
                meaning = tds[1].text.strip()
                said_info_per_table[code_figure] = meaning

            # Bit Number列の値を取得
            elif code_figure_text.startswith('Bit'):
                bit_number = int(re.match(r'Bit Number (\d+)', code_figure_text).group(1))
                meaning = tds[1].text.strip()
                said_info_per_table[f'{bit_number:04d}'] = meaning

            # All (数字)の場合
            elif re.match(r'All \(\d+\)', code_figure_text):
                all_number = int(re.match(r'All \((\d+)\)', code_figure_text).group(1))
                all_number_str = f'{all_number:0{len(str(all_number))}}1'
                meaning = tds[1].text.strip()
                said_info_per_table[all_number_str] = meaning

        # table IDとSAID情報をsaid_info辞書に追加
        said_info[table_id] = said_info_per_table

    return said_info

html_table = """<hr id="001003">
<h4>0-01-003 - WMOR</h4>
<h4>WMO Region number/geographical area</h4>
<table rules=groups>
 <thead>
  <tr>
    <th>Code figure</th>
    <th class="left">Meaning</th>
  </tr>
 </thead>
 <tbody>
  <tr>
    <td class="center">0</td>
    <td>Antarctica</td>
  </tr>
  <tr>
    <td class="center">1</td>
    <td>Region I</td>
  </tr>
  <tr>
    <td class="center">2</td>
    <td>Region II</td>
  </tr>
  <tr>
    <td class="center">3</td>
    <td>Region III</td>
  </tr>
  <tr>
    <td class="center">4</td>
    <td>Region IV</td>
  </tr>
  <tr>
    <td class="center">5</td>
    <td>Region V</td>
  </tr>
  <tr>
    <td class="center">6</td>
    <td>Region VI</td>
  </tr>
  <tr>
    <td class="center">7</td>
    <td>Missing value</td>
  </tr>
 </tbody>
</table>
<br />
<hr id="001007">
<h4>0-01-007 - SAID</h4>
<h4>Satellite identifier</h4>
<table rules=groups>
 <thead>
  <tr>
    <th>Code figure</th>
    <th class="left">Meaning</th>
  </tr>
 </thead>
 <tbody>
  <tr>
    <td class="center">0</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">1</td>
    <td>ERS 1</td>
  </tr>
  <tr>
    <td class="center">2</td>
    <td>ERS 2</td>
  </tr>
  <tr>
    <td class="center">3</td>
    <td>METOP-1 (Metop-B)</td>
  </tr>
  <tr>
    <td class="center">4</td>
    <td>METOP-2 (Metop-A)</td>
  </tr>
  <tr>
    <td class="center">5</td>
    <td>METOP-3 (Metop-C)</td>
  </tr>
  <tr>
    <td class="center">6-19</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">20</td>
    <td>SPOT1</td>
  </tr>
  <tr>
    <td class="center">21</td>
    <td>SPOT2</td>
  </tr>
  <tr>
    <td class="center">22</td>
    <td>SPOT3</td>
  </tr>
  <tr>
    <td class="center">23</td>
    <td>SPOT4</td>
  </tr>
  <tr>
    <td class="center">24-39</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">40</td>
    <td>OERSTED</td>
  </tr>
  <tr>
    <td class="center">41</td>
    <td>CHAMP</td>
  </tr>
  <tr>
    <td class="center">42</td>
    <td>TerraSAR-X</td>
  </tr>
  <tr>
    <td class="center">43</td>
    <td>TanDEM-X</td>
  </tr>
  <tr>
    <td class="center">44</td>
    <td>PAZ</td>
  </tr>
  <tr>
    <td class="center">45</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">46</td>
    <td>SMOS</td>
  </tr>
  <tr>
    <td class="center">47</td>
    <td>CryoSat-2</td>
  </tr>
  <tr>
    <td class="center">48</td>
    <td>AEOLUS</td>
  </tr>
  <tr>
    <td class="center">49</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">50</td>
    <td>METEOSAT 3</td>
  </tr>
  <tr>
    <td class="center">51</td>
    <td>METEOSAT 4</td>
  </tr>
  <tr>
    <td class="center">52</td>
    <td>METEOSAT 5</td>
  </tr>
  <tr>
    <td class="center">53</td>
    <td>METEOSAT 6</td>
  </tr>
  <tr>
    <td class="center">54</td>
    <td>METEOSAT 7</td>
  </tr>
  <tr>
    <td class="center">55</td>
    <td>METEOSAT 8</td>
  </tr>
  <tr>
    <td class="center">56</td>
    <td>METEOSAT 9</td>
  </tr>
  <tr>
    <td class="center">57</td>
    <td>METEOSAT 10</td>
  </tr>
  <tr>
    <td class="center">58</td>
    <td>METEOSAT 1</td>
  </tr>
  <tr>
    <td class="center">59</td>
    <td>METEOSAT 2</td>
  </tr>
  <tr>
    <td class="center">60</td>
    <td>ENVISAT</td>
  </tr>
  <tr>
    <td class="center">61</td>
    <td>Sentinel 3A</td>
  </tr>
  <tr>
    <td class="center">62</td>
    <td>Sentinel 1A</td>
  </tr>
  <tr>
    <td class="center">63</td>
    <td>Sentinel 1B</td>
  </tr>
  <tr>
    <td class="center">64</td>
    <td>Sentinel 5P</td>
  </tr>
  <tr>
    <td class="center">65</td>
    <td>Sentinel 3B</td>
  </tr>
  <tr>
    <td class="center">66-69</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">70</td>
    <td>METEOSAT 11</td>
  </tr>
  <tr>
    <td class="center">71-119</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">120</td>
    <td>ADEOS</td>
  </tr>
  <tr>
    <td class="center">121</td>
    <td>ADEOS II</td>
  </tr>
  <tr>
    <td class="center">122</td>
    <td>GCOM-W1</td>
  </tr>
  <tr>
    <td class="center">123-139</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">140</td>
    <td>GOSAT</td>
  </tr>
  <tr>
    <td class="center">141-149</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">150</td>
    <td>GMS 3</td>
  </tr>
  <tr>
    <td class="center">151</td>
    <td>GMS 4</td>
  </tr>
  <tr>
    <td class="center">152</td>
    <td>GMS 5</td>
  </tr>
  <tr>
    <td class="center">153</td>
    <td>GMS</td>
  </tr>
  <tr>
    <td class="center">154</td>
    <td>GMS-2</td>
  </tr>
  <tr>
    <td class="center">155-170</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">171</td>
    <td>MTSAT-1R</td>
  </tr>
  <tr>
    <td class="center">172</td>
    <td>MTSAT-2</td>
  </tr>
  <tr>
    <td class="center">173</td>
    <td>Himawari-8</td>
  </tr>
  <tr>
    <td class="center">174</td>
    <td>Himawari-9</td>
  </tr>
  <tr>
    <td class="center">175-199</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">200</td>
    <td>NOAA 8</td>
  </tr>
  <tr>
    <td class="center">201</td>
    <td>NOAA 9</td>
  </tr>
  <tr>
    <td class="center">202</td>
    <td>NOAA 10</td>
  </tr>
  <tr>
    <td class="center">203</td>
    <td>NOAA 11</td>
  </tr>
  <tr>
    <td class="center">204</td>
    <td>NOAA 12</td>
  </tr>
  <tr>
    <td class="center">205</td>
    <td>NOAA 14</td>
  </tr>
  <tr>
    <td class="center">206</td>
    <td>NOAA 15</td>
  </tr>
  <tr>
    <td class="center">207</td>
    <td>NOAA 16</td>
  </tr>
  <tr>
    <td class="center">208</td>
    <td>NOAA 17</td>
  </tr>
  <tr>
    <td class="center">209</td>
    <td>NOAA 18</td>
  </tr>
  <tr>
    <td class="center">210-219</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">220</td>
    <td>LANDSAT 5</td>
  </tr>
  <tr>
    <td class="center">221</td>
    <td>LANDSAT 4</td>
  </tr>
  <tr>
    <td class="center">222</td>
    <td>LANDSAT 7</td>
  </tr>
  <tr>
    <td class="center">223</td>
    <td>NOAA 19</td>
  </tr>
  <tr>
    <td class="center">224</td>
    <td>NPP</td>
  </tr>
  <tr>
    <td class="center">225</td>
    <td>NOAA 20</td>
  </tr>
  <tr>
    <td class="center">226</td>
    <td>NOAA 21</td>
  </tr>
  <tr>
    <td class="center">227-239</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">240</td>
    <td>DMSP 7</td>
  </tr>
  <tr>
    <td class="center">241</td>
    <td>DMSP 8</td>
  </tr>
  <tr>
    <td class="center">242</td>
    <td>DMSP 9</td>
  </tr>
  <tr>
    <td class="center">243</td>
    <td>DMSP 10</td>
  </tr>
  <tr>
    <td class="center">244</td>
    <td>DMSP 11</td>
  </tr>
  <tr>
    <td class="center">245</td>
    <td>DMSP 12</td>
  </tr>
  <tr>
    <td class="center">246</td>
    <td>DMSP 13</td>
  </tr>
  <tr>
    <td class="center">247</td>
    <td>DMSP 14</td>
  </tr>
  <tr>
    <td class="center">248</td>
    <td>DMSP 15</td>
  </tr>
  <tr>
    <td class="center">249</td>
    <td>DMSP 16</td>
  </tr>
  <tr>
    <td class="center">250</td>
    <td>GOES 6</td>
  </tr>
  <tr>
    <td class="center">251</td>
    <td>GOES 7</td>
  </tr>
  <tr>
    <td class="center">252</td>
    <td>GOES 8</td>
  </tr>
  <tr>
    <td class="center">253</td>
    <td>GOES 9</td>
  </tr>
  <tr>
    <td class="center">254</td>
    <td>GOES 10</td>
  </tr>
  <tr>
    <td class="center">255</td>
    <td>GOES 11</td>
  </tr>
  <tr>
    <td class="center">256</td>
    <td>GOES 12</td>
  </tr>
  <tr>
    <td class="center">257</td>
    <td>GOES 13</td>
  </tr>
  <tr>
    <td class="center">258</td>
    <td>GOES 14</td>
  </tr>
  <tr>
    <td class="center">259</td>
    <td>GOES 15</td>
  </tr>
  <tr>
    <td class="center">260</td>
    <td>JASON 1</td>
  </tr>
  <tr>
    <td class="center">261</td>
    <td>JASON 2</td>
  </tr>
  <tr>
    <td class="center">262</td>
    <td>JASON 3</td>
  </tr>
  <tr>
    <td class="center">263-268</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">269</td>
    <td>Spire Lemur 3U Cubesat</td>
  </tr>
  <tr>
    <td class="center">270</td>
    <td>GOES 16</td>
  </tr>
  <tr>
    <td class="center">271</td>
    <td>GOES 17</td>
  </tr>
  <tr>
    <td class="center">272</td>
    <td>GOES 18</td>
  </tr>
  <tr>
    <td class="center">273</td>
    <td>GOES 19</td>
  </tr>
  <tr>
    <td class="center">274-280</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">281</td>
    <td>QUIKSCAT</td>
  </tr>
  <tr>
    <td class="center">282</td>
    <td>TRMM</td>
  </tr>
  <tr>
    <td class="center">283</td>
    <td>CORIOLIS</td>
  </tr>
  <tr>
    <td class="center">284</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">285</td>
    <td>DMSP17</td>
  </tr>
  <tr>
    <td class="center">286</td>
    <td>DMSP18</td>
  </tr>
  <tr>
    <td class="center">287</td>
    <td>DMSP-19</td>
  </tr>
  <tr>
    <td class="center">288</td>
    <td>GPM-core</td>
  </tr>
  <tr>
    <td class="center">289</td>
    <td>Orbiting Carbon Observatory - 2 (OCO-2, NASA)</td>
  </tr>
  <tr>
    <td class="center">290-309</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">310</td>
    <td>GOMS 1</td>
  </tr>
  <tr>
    <td class="center">311</td>
    <td>GOMS 2</td>
  </tr>
  <tr>
    <td class="center">312-319</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">320</td>
    <td>METEOR 2-21</td>
  </tr>
  <tr>
    <td class="center">321</td>
    <td>METEOR 3-5</td>
  </tr>
  <tr>
    <td class="center">322</td>
    <td>METEOR 3M-1</td>
  </tr>
  <tr>
    <td class="center">323</td>
    <td>METEOR 3M-2</td>
  </tr>
  <tr>
    <td class="center">324-340</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">341</td>
    <td>RESURS 01-4</td>
  </tr>
  <tr>
    <td class="center">342-409</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">410</td>
    <td>KALPANA-1</td>
  </tr>
  <tr>
    <td class="center">411-420</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">421</td>
    <td>Oceansat-2</td>
  </tr>
  <tr>
    <td class="center">422</td>
    <td>ScatSat-1</td>
  </tr>
  <tr>
    <td class="center">423-421</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">422</td>
    <td>ScatSat-1</td>
  </tr>
  <tr>
    <td class="center">423</td>
    <td>Oceansat-3</td>
  </tr>
  <tr>
    <td class="center">424-429</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">430</td>
    <td>INSAT 1B</td>
  </tr>
  <tr>
    <td class="center">431</td>
    <td>INSAT 1C</td>
  </tr>
  <tr>
    <td class="center">432</td>
    <td>INSAT 1D</td>
  </tr>
  <tr>
    <td class="center">433-439</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">440</td>
    <td>Megha-Tropiques</td>
  </tr>
  <tr>
    <td class="center">441</td>
    <td>SARAL</td>
  </tr>
  <tr>
    <td class="center">442-449</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">450</td>
    <td>INSAT 2A</td>
  </tr>
  <tr>
    <td class="center">451</td>
    <td>INSAT 2B</td>
  </tr>
  <tr>
    <td class="center">452</td>
    <td>INSAT 2E</td>
  </tr>
  <tr>
    <td class="center">453-469</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">470</td>
    <td>INSAT 3A</td>
  </tr>
  <tr>
    <td class="center">471</td>
    <td>INSAT 3D</td>
  </tr>
  <tr>
    <td class="center">472</td>
    <td>INSAT 3E</td>
  </tr>
  <tr>
    <td class="center">473</td>
    <td>INSAT 3DR</td>
  </tr>
  <tr>
    <td class="center">474</td>
    <td>INSAT 3DS</td>
  </tr>
  <tr>
    <td class="center">475-499</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">500</td>
    <td>FY-1C</td>
  </tr>
  <tr>
    <td class="center">501</td>
    <td>FY-1D</td>
  </tr>
  <tr>
    <td class="center">502</td>
    <td>Hai Yang 2A (HY-2A, SOA/NSOAS China)</td>
  </tr>
  <tr>
    <td class="center">503</td>
    <td>Hai Yang 2B (HY-2B, SOA/NSOAS China)</td>
  </tr>
  <tr>
    <td class="center">504-509</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">510</td>
    <td>FY-2</td>
  </tr>
  <tr>
    <td class="center">511</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">512</td>
    <td>FY-2B</td>
  </tr>
  <tr>
    <td class="center">513</td>
    <td>FY-2C</td>
  </tr>
  <tr>
    <td class="center">514</td>
    <td>FY-2D</td>
  </tr>
  <tr>
    <td class="center">515</td>
    <td>FY-2E</td>
  </tr>
  <tr>
    <td class="center">516</td>
    <td>FY-2F</td>
  </tr>
  <tr>
    <td class="center">517</td>
    <td>FY-2G</td>
  </tr>
  <tr>
    <td class="center">518-519</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">520</td>
    <td>FY-3A</td>
  </tr>
  <tr>
    <td class="center">521</td>
    <td>FY-3B</td>
  </tr>
  <tr>
    <td class="center">522</td>
    <td>FY-3C</td>
  </tr>
  <tr>
    <td class="center">523</td>
    <td>FY-3D</td>
  </tr>
  <tr>
    <td class="center">524-529</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">530</td>
    <td>FY-4A</td>
  </tr>
  <tr>
    <td class="center">531-699</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">700</td>
    <td>TIROS M (ITOS 1)</td>
  </tr>
  <tr>
    <td class="center">701</td>
    <td>NOAA 1</td>
  </tr>
  <tr>
    <td class="center">702</td>
    <td>NOAA 2</td>
  </tr>
  <tr>
    <td class="center">703</td>
    <td>NOAA 3</td>
  </tr>
  <tr>
    <td class="center">704</td>
    <td>NOAA 4</td>
  </tr>
  <tr>
    <td class="center">705</td>
    <td>NOAA 5</td>
  </tr>
  <tr>
    <td class="center">706</td>
    <td>NOAA 6</td>
  </tr>
  <tr>
    <td class="center">707</td>
    <td>NOAA 7</td>
  </tr>
  <tr>
    <td class="center">708</td>
    <td>TIROS-N</td>
  </tr>
  <tr>
    <td class="center">709</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">710</td>
    <td>GOES (SMS 1)</td>
  </tr>
  <tr>
    <td class="center">711</td>
    <td>GOES (SMS 2)</td>
  </tr>
  <tr>
    <td class="center">712-719</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">720</td>
    <td>TOPEX</td>
  </tr>
  <tr>
    <td class="center">721</td>
    <td>GFO</td>
  </tr>
  <tr>
    <td class="center">722</td>
    <td>GRACE A</td>
  </tr>
  <tr>
    <td class="center">723</td>
    <td>GRACE B</td>
  </tr>
  <tr>
    <td class="center">724</td>
    <td>COSMIC-2 P1</td>
  </tr>
  <tr>
    <td class="center">725</td>
    <td>COSMIC-2 P2</td>
  </tr>
  <tr>
    <td class="center">726</td>
    <td>COSMIC-2 P3</td>
  </tr>
  <tr>
    <td class="center">727</td>
    <td>COSMIC-2 P4</td>
  </tr>
  <tr>
    <td class="center">728</td>
    <td>COSMIC-2 P5</td>
  </tr>
  <tr>
    <td class="center">729</td>
    <td>COSMIC-2 P6</td>
  </tr>
  <tr>
    <td class="center">730</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">731</td>
    <td>GOES 1</td>
  </tr>
  <tr>
    <td class="center">732</td>
    <td>GOES 2</td>
  </tr>
  <tr>
    <td class="center">733</td>
    <td>GOES 3</td>
  </tr>
  <tr>
    <td class="center">734</td>
    <td>GOES 4</td>
  </tr>
  <tr>
    <td class="center">735</td>
    <td>GOES 5</td>
  </tr>
  <tr>
    <td class="center">736-739</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">740</td>
    <td>COSMIC-1</td>
  </tr>
  <tr>
    <td class="center">741</td>
    <td>COSMIC-2</td>
  </tr>
  <tr>
    <td class="center">742</td>
    <td>COSMIC-3</td>
  </tr>
  <tr>
    <td class="center">743</td>
    <td>COSMIC-4</td>
  </tr>
  <tr>
    <td class="center">744</td>
    <td>COSMIC-5</td>
  </tr>
  <tr>
    <td class="center">745</td>
    <td>COSMIC-6</td>
  </tr>
  <tr>
    <td class="center">746-749</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">750</td>
    <td>COSMIC-2 E1</td>
  </tr>
  <tr>
    <td class="center">751</td>
    <td>COSMIC-2 E2</td>
  </tr>
  <tr>
    <td class="center">752</td>
    <td>COSMIC-2 E3</td>
  </tr>
  <tr>
    <td class="center">753</td>
    <td>COSMIC-2 E4</td>
  </tr>
  <tr>
    <td class="center">754</td>
    <td>COSMIC-2 E5</td>
  </tr>
  <tr>
    <td class="center">755</td>
    <td>COSMIC-2 E6</td>
  </tr>
  <tr>
    <td class="center">756-762</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">763</td>
    <td>NIMBUS 3</td>
  </tr>
  <tr>
    <td class="center">764</td>
    <td>NIMBUS 4</td>
  </tr>
  <tr>
    <td class="center">765</td>
    <td>NIMBUS 5</td>
  </tr>
  <tr>
    <td class="center">766</td>
    <td>NIMBUS 6</td>
  </tr>
  <tr>
    <td class="center">767</td>
    <td>NIMBUS 7</td>
  </tr>
  <tr>
    <td class="center">768-779</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">780</td>
    <td>ERBS</td>
  </tr>
  <tr>
    <td class="center">781</td>
    <td>UARS</td>
  </tr>
  <tr>
    <td class="center">782</td>
    <td>EARTH PROBE</td>
  </tr>
  <tr>
    <td class="center">783</td>
    <td>TERRA</td>
  </tr>
  <tr>
    <td class="center">784</td>
    <td>AQUA</td>
  </tr>
  <tr>
    <td class="center">785</td>
    <td>AURA</td>
  </tr>
  <tr>
    <td class="center">786</td>
    <td>C/NOFS</td>
  </tr>
  <tr>
    <td class="center">787</td>
    <td>CALIPSO</td>
  </tr>
  <tr>
    <td class="center">788</td>
    <td>CloudSat</td>
  </tr>
  <tr>
    <td class="center">789-799</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">800</td>
    <td>SUNSAT</td>
  </tr>
  <tr>
    <td class="center">801</td>
    <td>International Space Station (ISS)</td>
  </tr>
  <tr>
    <td class="center">802</td>
    <td>CFOSAT</td>
  </tr>
  <tr>
    <td class="center">803</td>
    <td>GRACE C (GRACE-FO)</td>
  </tr>
  <tr>
    <td class="center">804</td>
    <td>GRACE D (GRACE-FO)</td>
  </tr>
  <tr>
    <td class="center">805-809</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">810</td>
    <td>COMS-1</td>
  </tr>
  <tr>
    <td class="center">811</td>
    <td>COMS-2</td>
  </tr>
  <tr>
    <td class="center">812</td>
    <td>SCISAT-1</td>
  </tr>
  <tr>
    <td class="center">813</td>
    <td>ODIN</td>
  </tr>
  <tr>
    <td class="center">814-819</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">820</td>
    <td>SAC-C</td>
  </tr>
  <tr>
    <td class="center">821</td>
    <td>SAC-D</td>
  </tr>
  <tr>
    <td class="center">822-824</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">825</td>
    <td>KOMPSAT-5</td>
  </tr>
  <tr>
    <td class="center">826-849</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">850</td>
    <td>Combination of TERRA and AQUA</td>
  </tr>
  <tr>
    <td class="center">851</td>
    <td>Combination of NOAA 16 to NOAA 19</td>
  </tr>
  <tr>
    <td class="center">852</td>
    <td>Combination of METOP-1 to METOP-3</td>
  </tr>
  <tr>
    <td class="center">853</td>
    <td>Combination of METEOSAT and DMSP</td>
  </tr>
  <tr>
    <td class="center">854</td>
    <td>Non-specific mixture of geostationary and low earth orbiting satellites</td>
  </tr>
  <tr>
    <td class="center">855</td>
    <td>Combination of INSAT 3D and INSAT 3DR</td>
  </tr>
  <tr>
    <td class="center">856-1022</td>
    <td>Reserved</td>
  </tr>
  <tr>
    <td class="center">1023</td>
    <td>Missing value</td>
  </tr>
 </tbody>
</table>
<br />
# <hr id="001024">
# <h4>0-01-024 - WSPDS</h4>
# <h4>Wind speed source</h4>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No wind speed data available</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>AMSR-E data</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>TMI data</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>NWP: ECMWF</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>NWP: UK Met Office</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>NWP: NCEP</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>Reference climatology</td>
#   </tr>
#   <tr>
#     <td class="center">7</td>
#     <td>ERS_Scatterometer</td>
#   </tr>
#   <tr>
#     <td class="center">8-30</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001028">
# <h4>0-01-028 - AODS</h4>
# <h4>Aerosol optical depth (AOD) source</h4>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No AOD data available</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>NESDIS</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>NAVOCEANO</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>NAAPS</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>MERIS</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>AATSR</td>
#   </tr>
#   <tr>
#     <td class="center">6-30</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001029">
# <h4>0-01-029 - SSIS</h4>
# <h4>SSI source</h4>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No SSI data available</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>MSG_SEVIRI</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>GOES East</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>GOES West</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>ECMWF</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>NCEP</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>UK Met Office</td>
#   </tr>
#   <tr>
#     <td class="center">7-30</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001031">
# <h4>0-01-031 - GCLONG</h4>
# <h4>Identification of originating/generating centre</h4>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>WMO Secretariat</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">7</td>
#     <td>U.S. National Weather Service, National Centres for Environmental Prediction (NCEP)</td>
#   </tr>
#   <tr>
#     <td class="center">8</td>
#     <td>U.S. National Weather Service Telecommunications Gateway (NWSTG)</td>
#   </tr>
#   <tr>
#     <td class="center">9</td>
#     <td>U.S. National Weather Service - Other</td>
#   </tr>
#   <tr>
#     <td class="center">10</td>
#     <td>Cairo (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">11</td>
#     <td>Cairo (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">12</td>
#     <td>Dakar (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">13</td>
#     <td>Dakar (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">14</td>
#     <td>Nairobi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">15</td>
#     <td>Nairobi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">16</td>
#     <td>Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">17</td>
#     <td>Tunis (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">18</td>
#     <td>Tunis Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">19</td>
#     <td>Tunis Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">20</td>
#     <td>Las Palmas</td>
#   </tr>
#   <tr>
#     <td class="center">21</td>
#     <td>Algiers (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">22</td>
#     <td>ACMAD</td>
#   </tr>
#   <tr>
#     <td class="center">23</td>
#     <td>Mozambique (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">24</td>
#     <td>Pretoria (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">25</td>
#     <td>La Réunion (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">26</td>
#     <td>Khabarovsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">27</td>
#     <td>Khabarovsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">28</td>
#     <td>New Delhi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">29</td>
#     <td>New Delhi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">30</td>
#     <td>Novosibirsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Novosibirsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">32</td>
#     <td>Tashkent (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">33</td>
#     <td>Jeddah (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">34</td>
#     <td>Tokyo (RSMC), Japan Meteorological Agency</td>
#   </tr>
#   <tr>
#     <td class="center">35</td>
#     <td>Tokyo (RSMC), Japan Meteorological Agency</td>
#   </tr>
#   <tr>
#     <td class="center">36</td>
#     <td>Bangkok</td>
#   </tr>
#   <tr>
#     <td class="center">37</td>
#     <td>Ulaanbaatar</td>
#   </tr>
#   <tr>
#     <td class="center">38</td>
#     <td>Beijing (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">39</td>
#     <td>Beijing (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">40</td>
#     <td>Seoul</td>
#   </tr>
#   <tr>
#     <td class="center">41</td>
#     <td>Buenos Aires (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">42</td>
#     <td>Buenos Aires (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">43</td>
#     <td>Brasilia (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">44</td>
#     <td>Brasilia (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">45</td>
#     <td>Santiago</td>
#   </tr>
#   <tr>
#     <td class="center">46</td>
#     <td>Brazilian Space Agency ­ INPE</td>
#   </tr>
#   <tr>
#     <td class="center">47</td>
#     <td>Colombia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">48</td>
#     <td>Ecuador (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">49</td>
#     <td>Peru (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">50</td>
#     <td>Venezuela (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">51</td>
#     <td>Miami (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">52</td>
#     <td>Miami (RSMC), National Hurricane Center</td>
#   </tr>
#   <tr>
#     <td class="center">53</td>
#     <td>MSC Monitoring</td>
#   </tr>
#   <tr>
#     <td class="center">54</td>
#     <td>Montreal (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">55</td>
#     <td>San Francisco</td>
#   </tr>
#   <tr>
#     <td class="center">56</td>
#     <td>ARINC Centre</td>
#   </tr>
#   <tr>
#     <td class="center">57</td>
#     <td>U.S. Air Force Global Weather Central</td>
#   </tr>
#   <tr>
#     <td class="center">58</td>
#     <td>Fleet Numerical Meteorology and Oceanography Center, Monterey, CA, USA</td>
#   </tr>
#   <tr>
#     <td class="center">59</td>
#     <td>NOAA Forecast Systems Laboratory, Boulder, CO, USA</td>
#   </tr>
#   <tr>
#     <td class="center">60</td>
#     <td>United States National Centre for Atmospheric Research (NCAR)</td>
#   </tr>
#   <tr>
#     <td class="center">61</td>
#     <td>Service ARGOS - Landover</td>
#   </tr>
#   <tr>
#     <td class="center">62</td>
#     <td>U.S. Naval Oceanographic Office</td>
#   </tr>
#   <tr>
#     <td class="center">63</td>
#     <td>International Research Institute for Climate and Society (IRI)</td>
#   </tr>
#   <tr>
#     <td class="center">64</td>
#     <td>Honolulu (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">65</td>
#     <td>Darwin (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">66</td>
#     <td>Darwin (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">67</td>
#     <td>Melbourne (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">68</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">69</td>
#     <td>Wellington (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">70</td>
#     <td>Wellington (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">71</td>
#     <td>Nadi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">72</td>
#     <td>Singapore</td>
#   </tr>
#   <tr>
#     <td class="center">73</td>
#     <td>Malaysia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">74</td>
#     <td>UK Meteorological Office, Exeter (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">75</td>
#     <td>UK Meteorological Office, Exeter (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">76</td>
#     <td>Moscow (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">77</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">78</td>
#     <td>Offenbach (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">79</td>
#     <td>Offenbach (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">80</td>
#     <td>Rome (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">81</td>
#     <td>Rome (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">82</td>
#     <td>Norrköping</td>
#   </tr>
#   <tr>
#     <td class="center">83</td>
#     <td>Norrköping</td>
#   </tr>
#   <tr>
#     <td class="center">84</td>
#     <td>Toulouse (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">85</td>
#     <td>Toulouse (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">86</td>
#     <td>Helsinki</td>
#   </tr>
#   <tr>
#     <td class="center">87</td>
#     <td>Belgrade</td>
#   </tr>
#   <tr>
#     <td class="center">88</td>
#     <td>Oslo</td>
#   </tr>
#   <tr>
#     <td class="center">89</td>
#     <td>Prague</td>
#   </tr>
#   <tr>
#     <td class="center">90</td>
#     <td>Episkopi</td>
#   </tr>
#   <tr>
#     <td class="center">91</td>
#     <td>Ankara</td>
#   </tr>
#   <tr>
#     <td class="center">92</td>
#     <td>Frankfurt/Main</td>
#   </tr>
#   <tr>
#     <td class="center">93</td>
#     <td>London (WAFC)</td>
#   </tr>
#   <tr>
#     <td class="center">94</td>
#     <td>Copenhagen</td>
#   </tr>
#   <tr>
#     <td class="center">95</td>
#     <td>Rota</td>
#   </tr>
#   <tr>
#     <td class="center">96</td>
#     <td>Athens</td>
#   </tr>
#   <tr>
#     <td class="center">97</td>
#     <td>European Space Agency (ESA)</td>
#   </tr>
#   <tr>
#     <td class="center">98</td>
#     <td>European Centre for Medium-Range Weather Forecasts (ECMWF)</td>
#   </tr>
#   <tr>
#     <td class="center">99</td>
#     <td>De Bilt</td>
#   </tr>
#   <tr>
#     <td class="center">100</td>
#     <td>Brazzaville</td>
#   </tr>
#   <tr>
#     <td class="center">101</td>
#     <td>Abidjan</td>
#   </tr>
#   <tr>
#     <td class="center">102</td>
#     <td>Libya (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">103</td>
#     <td>Madagascar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">104</td>
#     <td>Mauritius (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">105</td>
#     <td>Niger (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">106</td>
#     <td>Seychelles (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">107</td>
#     <td>Uganda (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">108</td>
#     <td>Tanzania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">109</td>
#     <td>Zimbabwe (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">110</td>
#     <td>Hong-Kong, China</td>
#   </tr>
#   <tr>
#     <td class="center">111</td>
#     <td>Afghanistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">112</td>
#     <td>Bahrain (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">113</td>
#     <td>Bangladesh (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">114</td>
#     <td>Bhutan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">115</td>
#     <td>Cambodia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">116</td>
#     <td>Democratic People's Republic of Korea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">117</td>
#     <td>Islamic Republic of Iran (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">118</td>
#     <td>Iraq (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">119</td>
#     <td>Kazakhstan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">120</td>
#     <td>Kuwait (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">121</td>
#     <td>Kyrgyzstan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">122</td>
#     <td>Lao People's Democratic Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">123</td>
#     <td>Macao, China</td>
#   </tr>
#   <tr>
#     <td class="center">124</td>
#     <td>Maldives (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">125</td>
#     <td>Myanmar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">126</td>
#     <td>Nepal (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">127</td>
#     <td>Oman (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">128</td>
#     <td>Pakistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">129</td>
#     <td>Qatar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">130</td>
#     <td>Republic of Yemen (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">131</td>
#     <td>Sri Lanka (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">132</td>
#     <td>Tajikistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">133</td>
#     <td>Turkmenistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">134</td>
#     <td>United Arab Emirates (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">135</td>
#     <td>Uzbekistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">136</td>
#     <td>Viet Nam (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">137-139</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">140</td>
#     <td>Bolivia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">141</td>
#     <td>Guyana (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">142</td>
#     <td>Paraguay (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">143</td>
#     <td>Suriname (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">144</td>
#     <td>Uruguay (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">145</td>
#     <td>French Guyana</td>
#   </tr>
#   <tr>
#     <td class="center">146</td>
#     <td>Brazilian Navy Hydrographic Centre</td>
#   </tr>
#   <tr>
#     <td class="center">147</td>
#     <td>COmision Nacional de Actividades Espaciales (CONAE) - Argentina</td>
#   </tr>
#   <tr>
#     <td class="center">148-149</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">150</td>
#     <td>Antigua and Barbuda (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">151</td>
#     <td>Bahamas (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">152</td>
#     <td>Barbados (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">153</td>
#     <td>Belize (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">154</td>
#     <td>British Caribbean Territories Centre</td>
#   </tr>
#   <tr>
#     <td class="center">155</td>
#     <td>San Jose</td>
#   </tr>
#   <tr>
#     <td class="center">156</td>
#     <td>Cuba (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">157</td>
#     <td>Dominica (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">158</td>
#     <td>Dominican Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">159</td>
#     <td>El Salvador (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">160</td>
#     <td>U.S. NOAA/NESDIS</td>
#   </tr>
#   <tr>
#     <td class="center">161</td>
#     <td>U.S. NOAA Office of Oceanic and Atmospheric Research</td>
#   </tr>
#   <tr>
#     <td class="center">162</td>
#     <td>Guatemala (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">163</td>
#     <td>Haiti (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">164</td>
#     <td>Honduras (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">165</td>
#     <td>Jamaica (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">166</td>
#     <td>Mexico</td>
#   </tr>
#   <tr>
#     <td class="center">167</td>
#     <td>Curaçao and Sint Maarten (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">168</td>
#     <td>Nicaragua (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">169</td>
#     <td>Panama (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">170</td>
#     <td>Saint Lucia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">171</td>
#     <td>Trinidad and Tobago (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">172</td>
#     <td>French Departments in RA IV</td>
#   </tr>
#   <tr>
#     <td class="center">173</td>
#     <td>U.S. National Aeronautics and Space Administration (NASA)</td>
#   </tr>
#   <tr>
#     <td class="center">174</td>
#     <td>Integrated System Data Management/Marine Environmental Data Service (ISDM/MEDS - Canada)</td>
#   </tr>
#   <tr>
#     <td class="center">175</td>
#     <td>University Corporation for Atmospheric Research (UCAR) - United States</td>
#   </tr>
#   <tr>
#     <td class="center">176</td>
#     <td>U.S. Cooperative Institute for Meteorological Satellite Studies (CIMSS)</td>
#   </tr>
#   <tr>
#     <td class="center">177</td>
#     <td>U.S. NOAA National Ocean Service</td>
#   </tr>
#   <tr>
#     <td class="center">178</td>
#     <td>Spire Global, Inc.</td>
#   </tr>
#   <tr>
#     <td class="center">179-189</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">190</td>
#     <td>Cook Islands (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">191</td>
#     <td>French Polynesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">192</td>
#     <td>Tonga (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">193</td>
#     <td>Vanuatu (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">194</td>
#     <td>Brunei Darussalam (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">195</td>
#     <td>Indonesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">196</td>
#     <td>Kiribati (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">197</td>
#     <td>Federated States of Micronesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">198</td>
#     <td>New Caledonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">199</td>
#     <td>Niue</td>
#   </tr>
#   <tr>
#     <td class="center">200</td>
#     <td>Papua New Guinea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">201</td>
#     <td>Philippines (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">202</td>
#     <td>Samoa (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">203</td>
#     <td>Solomon Islands (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">204</td>
#     <td>National Institute of Water and Atmospheric Research  (NIWA – New Zealand)</td>
#   </tr>
#   <tr>
#     <td class="center">205-209</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">210</td>
#     <td>Frascati (ESA/ESRIN)</td>
#   </tr>
#   <tr>
#     <td class="center">211</td>
#     <td>Lannion</td>
#   </tr>
#   <tr>
#     <td class="center">212</td>
#     <td>Lisboa</td>
#   </tr>
#   <tr>
#     <td class="center">213</td>
#     <td>Reykiavik</td>
#   </tr>
#   <tr>
#     <td class="center">214</td>
#     <td>Madrid</td>
#   </tr>
#   <tr>
#     <td class="center">215</td>
#     <td>Zürich</td>
#   </tr>
#   <tr>
#     <td class="center">216</td>
#     <td>Service ARGOS Toulouse</td>
#   </tr>
#   <tr>
#     <td class="center">217</td>
#     <td>Bratislava</td>
#   </tr>
#   <tr>
#     <td class="center">218</td>
#     <td>Budapest</td>
#   </tr>
#   <tr>
#     <td class="center">219</td>
#     <td>Ljubljana</td>
#   </tr>
#   <tr>
#     <td class="center">220</td>
#     <td>Warsaw</td>
#   </tr>
#   <tr>
#     <td class="center">221</td>
#     <td>Zagreb</td>
#   </tr>
#   <tr>
#     <td class="center">222</td>
#     <td>Albania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">223</td>
#     <td>Armenia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">224</td>
#     <td>Austria (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">225</td>
#     <td>Azerbaijan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">226</td>
#     <td>Belarus (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">227</td>
#     <td>Belgium (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">228</td>
#     <td>Bosnia and Herzegovina (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">229</td>
#     <td>Bulgaria (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">230</td>
#     <td>Cyprus (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">231</td>
#     <td>Estonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">232</td>
#     <td>Georgia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">233</td>
#     <td>Dublin</td>
#   </tr>
#   <tr>
#     <td class="center">234</td>
#     <td>Israel (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">235</td>
#     <td>Jordan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">236</td>
#     <td>Latvia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">237</td>
#     <td>Lebanon (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">238</td>
#     <td>Lithuania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">239</td>
#     <td>Luxembourg</td>
#   </tr>
#   <tr>
#     <td class="center">240</td>
#     <td>Malta (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">241</td>
#     <td>Monaco</td>
#   </tr>
#   <tr>
#     <td class="center">242</td>
#     <td>Romania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">243</td>
#     <td>Syrian Arab Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">244</td>
#     <td>The former Yugoslav Republic of Macedonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">245</td>
#     <td>Ukraine (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">246</td>
#     <td>Republic of Moldova (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">247</td>
#     <td>Operational Programme for the Exchange of weather RAdar information (OPERA) - EUMETNET</td>
#   </tr>
#   <tr>
#     <td class="center">248</td>
#     <td>Montenegro (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">249</td>
#     <td>Barcelona Dust Forecast Center</td>
#   </tr>
#   <tr>
#     <td class="center">250</td>
#     <td>COnsortium for Small scale MOdelling  (COSMO)</td>
#   </tr>
#   <tr>
#     <td class="center">251</td>
#     <td>Meteorological Cooperation on Operational NWP (MetCoOp)</td>
#   </tr>
#   <tr>
#     <td class="center">252</td>
#     <td>Max Planck Institute for Meteorology (MPI-M)</td>
#   </tr>
#   <tr>
#     <td class="center">253</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">254</td>
#     <td>EUMETSAT Operation Centre</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">256</td>
#     <td>Angola (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">257</td>
#     <td>Benin (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">258</td>
#     <td>Botswana (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">259</td>
#     <td>Burkina Faso (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">260</td>
#     <td>Burundi (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">261</td>
#     <td>Cameroon (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">262</td>
#     <td>Cape Verde (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">263</td>
#     <td>Central African Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">264</td>
#     <td>Chad (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">265</td>
#     <td>Comoros (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">266</td>
#     <td>Democratic Republic of the Congo (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">267</td>
#     <td>Djibouti (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">268</td>
#     <td>Eritrea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">269</td>
#     <td>Ethiopia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">270</td>
#     <td>Gabon (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">271</td>
#     <td>Gambia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">272</td>
#     <td>Ghana (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">273</td>
#     <td>Guinea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">274</td>
#     <td>Guinea Bissau (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">275</td>
#     <td>Lesotho (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">276</td>
#     <td>Liberia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">277</td>
#     <td>Malawi (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">278</td>
#     <td>Mali (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">279</td>
#     <td>Mauritania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">280</td>
#     <td>Namibia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">281</td>
#     <td>Nigeria (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">282</td>
#     <td>Rwanda (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">283</td>
#     <td>Sao Tome and Principe (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">284</td>
#     <td>Sierra Leone (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">285</td>
#     <td>Somalia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">286</td>
#     <td>Sudan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">287</td>
#     <td>Swaziland (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">288</td>
#     <td>Togo (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">289</td>
#     <td>Zambia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">290-65534</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">65535</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001032">
# <h4>0-01-032 - GNAP</h4>
# <h4>Generating application</h4>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 160 (U.S. NOAA/NESDIS)</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>First guess</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, excluding the forecast consistency test, but with slight differences between the different satellite operators</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Quality values derived from the NESDIS RFF (Recursive Filter Function) method</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, with the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>Quality values derived from the NESDIS EE (Expected Error) method</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, excluding the forecast consistency test, and common to all satellite operators (computed exactly the same way)</td>
#   </tr>
#   <tr>
#     <td class="center">6-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 98 (European Centre for Medium-Range Weather Forecasts (ECMWF))</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0-60</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">61</td>
#     <td>3DVAR analysis</td>
#   </tr>
#   <tr>
#     <td class="center">62-64</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">65</td>
#     <td>4DVAR analysis</td>
#   </tr>
#   <tr>
#     <td class="center">66-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 34 (Tokyo (RSMC), Japan Meteorological Agency)</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0-100</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">101</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, with the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">102</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, excluding the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">103</td>
#     <td>Quality values derived from the NESDIS RFF (Recursive Filter Function) method</td>
#   </tr>
#   <tr>
#     <td class="center">104-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 176 (U.S. Cooperative Institute for Meteorological Satellite Studies (CIMSS))</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, excluding the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Quality values derived from the NESDIS RFF (Recursive Filter Function) method</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, with the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">4-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 7 (U.S. National Weather Service, National Centres for Environmental Prediction (NCEP))</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0-1</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Ultra Violet Index Model</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>NCEP/ARL Transport and Dispersion Model</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>NCEP/ARL Smoke Model</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Satellite-derived precipitation and temperature from IR</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>NCEP/ARL Dust Model</td>
#   </tr>
#   <tr>
#     <td class="center">7-9</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">10</td>
#     <td>Global Wind-Wave Forecast Model</td>
#   </tr>
#   <tr>
#     <td class="center">11</td>
#     <td>Global Multi-Grid Wave Model (Static Grids)</td>
#   </tr>
#   <tr>
#     <td class="center">12</td>
#     <td>Probabilistic Storm Surge</td>
#   </tr>
#   <tr>
#     <td class="center">13</td>
#     <td>Hurricane Multi-Grid Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">14</td>
#     <td>Extratropical Storm Surge Model</td>
#   </tr>
#   <tr>
#     <td class="center">15-18</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">19</td>
#     <td>Limited-area Fine Mesh (LFM) analysis</td>
#   </tr>
#   <tr>
#     <td class="center">20-24</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">25</td>
#     <td>Snow Cover Analysis</td>
#   </tr>
#   <tr>
#     <td class="center">26-29</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">30</td>
#     <td>Forecaster generated field</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Value added post processed field</td>
#   </tr>
#   <tr>
#     <td class="center">32-38</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">39</td>
#     <td>Nested Grid Forecast Model (NGM)</td>
#   </tr>
#   <tr>
#     <td class="center">40-41</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">42</td>
#     <td>Global Optimum Interpolation Analysis (GOI) from GFS model</td>
#   </tr>
#   <tr>
#     <td class="center">43</td>
#     <td>Global Optimum Interpolation Analysis (GOI) from "Final" run</td>
#   </tr>
#   <tr>
#     <td class="center">44</td>
#     <td>Sea Surface Temperature Analysis</td>
#   </tr>
#   <tr>
#     <td class="center">45</td>
#     <td>Coastal Ocean Circulation Model</td>
#   </tr>
#   <tr>
#     <td class="center">46</td>
#     <td>HYCOM - Global</td>
#   </tr>
#   <tr>
#     <td class="center">47</td>
#     <td>HYCOM - North Pacific basin</td>
#   </tr>
#   <tr>
#     <td class="center">48</td>
#     <td>HYCOM - North Atlantic basin</td>
#   </tr>
#   <tr>
#     <td class="center">49</td>
#     <td>Ozone Analysis from TIROS Observations</td>
#   </tr>
#   <tr>
#     <td class="center">50-51</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">52</td>
#     <td>Ozone Analysis from Nimbus 7 Observations</td>
#   </tr>
#   <tr>
#     <td class="center">53</td>
#     <td>LFM-Fourth Order Forecast Model</td>
#   </tr>
#   <tr>
#     <td class="center">54-63</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">64</td>
#     <td>Regional Optimum Interpolation Analysis (ROI)</td>
#   </tr>
#   <tr>
#     <td class="center">65-67</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">68</td>
#     <td>80 wave triangular, 18-layer Spectral model from GFS model</td>
#   </tr>
#   <tr>
#     <td class="center">69</td>
#     <td>80 wave triangular, 18 layer Spectral model from "Medium Range Forecast</td>
#   </tr>
#   <tr>
#     <td class="center">70</td>
#     <td>Quasi-Lagrangian Hurricane Model (QLM)</td>
#   </tr>
#   <tr>
#     <td class="center">71</td>
#     <td>Hurricane Weather Research and Forecasting (HWRF) Model</td>
#   </tr>
#   <tr>
#     <td class="center">72</td>
#     <td>Hurricane Non-Hydrostatic Multiscale Model on the B Grid (HNMMB)</td>
#   </tr>
#   <tr>
#     <td class="center">73</td>
#     <td>Fog Forecast model - Ocean Products Center</td>
#   </tr>
#   <tr>
#     <td class="center">74</td>
#     <td>Gulf of Mexico Wind/Wave</td>
#   </tr>
#   <tr>
#     <td class="center">75</td>
#     <td>Gulf of Alaska Wind/Wave</td>
#   </tr>
#   <tr>
#     <td class="center">76</td>
#     <td>Bias-corrected Medium Range Forecast</td>
#   </tr>
#   <tr>
#     <td class="center">77</td>
#     <td>126 wave triangular, 28 layer Spectral model from GFS model</td>
#   </tr>
#   <tr>
#     <td class="center">78</td>
#     <td>126 wave triangular, 28 layer Spectral model from "Medium Range Forecast" run</td>
#   </tr>
#   <tr>
#     <td class="center">79</td>
#     <td>Backup from the previous run</td>
#   </tr>
#   <tr>
#     <td class="center">80</td>
#     <td>62 wave triangular, 28 layer Spectral model from "Medium Range Forecast" run</td>
#   </tr>
#   <tr>
#     <td class="center">81</td>
#     <td>Analysis from GFS (Global Forecast System)</td>
#   </tr>
#   <tr>
#     <td class="center">82</td>
#     <td>Analysis from GDAS (Global Data Assimilation System)</td>
#   </tr>
#   <tr>
#     <td class="center">83</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">84</td>
#     <td>MESO NAM Model (currently 12 km)</td>
#   </tr>
#   <tr>
#     <td class="center">85</td>
#     <td>Real Time Ocean Forecast System (RTOFS)</td>
#   </tr>
#   <tr>
#     <td class="center">86</td>
#     <td>RUC Model, from Forecast Systems Lab (isentropic; scale: 60km at 40N)</td>
#   </tr>
#   <tr>
#     <td class="center">87</td>
#     <td>CAC Ensemble Forecasts from Spectral (ENSMB)</td>
#   </tr>
#   <tr>
#     <td class="center">88</td>
#     <td>NOAA Wave Watch III (NWW3) Ocean Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">89</td>
#     <td>Non-hydrostatic Meso Model (NMM) (Currently 8 km)</td>
#   </tr>
#   <tr>
#     <td class="center">90</td>
#     <td>62 wave triangular, 28 layer spectral model extension of the "Medium Range Forecast" run</td>
#   </tr>
#   <tr>
#     <td class="center">91-89</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">90</td>
#     <td>62 wave triangular, 28 layer spectral model extension of the "Medium Range Forecast" run</td>
#   </tr>
#   <tr>
#     <td class="center">91</td>
#     <td>62 wave triangular, 28 layer spectral model extension of the GFS model</td>
#   </tr>
#   <tr>
#     <td class="center">92</td>
#     <td>62 wave triangular, 28 layer spectral model run from the "Medium Range Forecast" final analysis</td>
#   </tr>
#   <tr>
#     <td class="center">93</td>
#     <td>62 wave triangular, 28 layer spectral model run from the T62 GDAS analysis of the "Medium Range Forecast" run</td>
#   </tr>
#   <tr>
#     <td class="center">94</td>
#     <td>T170/L42 Global Spectral Model from MRF run</td>
#   </tr>
#   <tr>
#     <td class="center">95</td>
#     <td>T126/L42 Global Spectral Model from MRF run</td>
#   </tr>
#   <tr>
#     <td class="center">96</td>
#     <td>Global Forecast System Model (T574 - forecast hours 000-192, T190 - forecast hours 204-384)</td>
#   </tr>
#   <tr>
#     <td class="center">97</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">98</td>
#     <td>Climate Forecast System Model -- Atmospheric model (GFS) coupled to a multi-level ocean model (currently GFS spectral model at T62, 64 levels coupled to 40 level MOM3 ocean model)</td>
#   </tr>
#   <tr>
#     <td class="center">99</td>
#     <td>Miscellaneous Test ID</td>
#   </tr>
#   <tr>
#     <td class="center">100</td>
#     <td>RUC Surface Analysis (scale: 60km at 40N)</td>
#   </tr>
#   <tr>
#     <td class="center">101</td>
#     <td>RUC Surface Analysis (scale: 40km at 40N)</td>
#   </tr>
#   <tr>
#     <td class="center">102-104</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">105</td>
#     <td>RUC Model from FSL (isentropic; scale: 20km at 40N)</td>
#   </tr>
#   <tr>
#     <td class="center">106</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">107</td>
#     <td>Global Ensemble Forecast System (GEFS)</td>
#   </tr>
#   <tr>
#     <td class="center">108</td>
#     <td>LAMP</td>
#   </tr>
#   <tr>
#     <td class="center">109</td>
#     <td>RTMA (Real Time Mesoscale Analysis)</td>
#   </tr>
#   <tr>
#     <td class="center">110</td>
#     <td>NAM Model - 15km version</td>
#   </tr>
#   <tr>
#     <td class="center">111</td>
#     <td>NAM model, generic resolution (used in SREF processing)</td>
#   </tr>
#   <tr>
#     <td class="center">112</td>
#     <td>WRF-NMM model, generic resolution (used in various runs) NMM=Nondydrostatic Mesoscale Model (NCEP)</td>
#   </tr>
#   <tr>
#     <td class="center">113</td>
#     <td>Products from NCEP SREF processing</td>
#   </tr>
#   <tr>
#     <td class="center">114</td>
#     <td>NAEFS Products from joined NCEP, CMC global ensembles</td>
#   </tr>
#   <tr>
#     <td class="center">115</td>
#     <td>Downscaled GFS from NAM eXtension</td>
#   </tr>
#   <tr>
#     <td class="center">116</td>
#     <td>WRF-EM model, generic resolution (used in various runs) EM - Eulerian Mass-core (NCAR - aka Advanced Research WRF)</td>
#   </tr>
#   <tr>
#     <td class="center">117</td>
#     <td>NEMS GFS Aerosol Component</td>
#   </tr>
#   <tr>
#     <td class="center">118</td>
#     <td>URMA (UnRestricted Mesoscale Analysis)</td>
#   </tr>
#   <tr>
#     <td class="center">119</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">120</td>
#     <td>Ice Concentration Analysis</td>
#   </tr>
#   <tr>
#     <td class="center">121</td>
#     <td>Western North Atlantic Regional Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">122</td>
#     <td>Alaska Waters Regional Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">123</td>
#     <td>North Atlantic Hurricane Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">124</td>
#     <td>Eastern North Pacific Regional Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">125</td>
#     <td>North Pacific Hurricane Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">126</td>
#     <td>Sea Ice Forecast Model</td>
#   </tr>
#   <tr>
#     <td class="center">127</td>
#     <td>Lake Ice Forecast Model</td>
#   </tr>
#   <tr>
#     <td class="center">128</td>
#     <td>Global Ocean Forecast Model</td>
#   </tr>
#   <tr>
#     <td class="center">129</td>
#     <td>Global Ocean Data Analysis System (GODAS)</td>
#   </tr>
#   <tr>
#     <td class="center">130</td>
#     <td>Merge of fields from the RUC, NAM, and Spectral Model</td>
#   </tr>
#   <tr>
#     <td class="center">131</td>
#     <td>Great Lakes Wave Model</td>
#   </tr>
#   <tr>
#     <td class="center">132-139</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">140</td>
#     <td>North American Regional Reanalysis (NARR)</td>
#   </tr>
#   <tr>
#     <td class="center">141</td>
#     <td>Land Data Assimilation and Forecast System</td>
#   </tr>
#   <tr>
#     <td class="center">142-149</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">150</td>
#     <td>NWS River Forecast System (NWSRFS)</td>
#   </tr>
#   <tr>
#     <td class="center">151</td>
#     <td>NWS Flash Flood Guidance System (NWSFFGS)</td>
#   </tr>
#   <tr>
#     <td class="center">152</td>
#     <td>WSR-88D Stage II Precipitation Analysis</td>
#   </tr>
#   <tr>
#     <td class="center">153</td>
#     <td>WSR-88D Stage III Precipitation Analysis</td>
#   </tr>
#   <tr>
#     <td class="center">154-179</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">180</td>
#     <td>Quantitative Precipitation Forecast generated by NCEP</td>
#   </tr>
#   <tr>
#     <td class="center">181</td>
#     <td>River Forecast Center Quantitative Precipitation Forecast mosaic generated by NCEP</td>
#   </tr>
#   <tr>
#     <td class="center">182</td>
#     <td>River Forecast Center Quantitative Precipitation Estimate mosaic generated by NCEP</td>
#   </tr>
#   <tr>
#     <td class="center">183</td>
#     <td>NDFD product generated by NCEP/HPC</td>
#   </tr>
#   <tr>
#     <td class="center">184</td>
#     <td>Climatological Calibrated Precipitation Analysis - CCPA</td>
#   </tr>
#   <tr>
#     <td class="center">185-189</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">190</td>
#     <td>National Convective Weather Diagnostic generated by NCEP/AWC</td>
#   </tr>
#   <tr>
#     <td class="center">191</td>
#     <td>Current Icing Potential automated product genterated by NCEP/AWC</td>
#   </tr>
#   <tr>
#     <td class="center">192</td>
#     <td>Analysis product from NCEP/AWC</td>
#   </tr>
#   <tr>
#     <td class="center">193</td>
#     <td>Forecast product from NCEP/AWC</td>
#   </tr>
#   <tr>
#     <td class="center">194</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">195</td>
#     <td>Climate Data Assimilation System 2 (CDAS2)</td>
#   </tr>
#   <tr>
#     <td class="center">196</td>
#     <td>Climate Data Assimilation System 2 (CDAS2) - used for regeneration runs</td>
#   </tr>
#   <tr>
#     <td class="center">197</td>
#     <td>Climate Data Assimilation System (CDAS)</td>
#   </tr>
#   <tr>
#     <td class="center">198</td>
#     <td>Climate Data Assimilation System (CDAS) - used for regeneration runs</td>
#   </tr>
#   <tr>
#     <td class="center">199</td>
#     <td>Climate Forecast System Reanalysis (CFSR) -- Atmospheric model (GFS) coupled to a multi-level ocean, land and seaice model (currently GFS spectral model at T382, 64 levels coupled to 40 level MOM4 ocean model)</td>
#   </tr>
#   <tr>
#     <td class="center">200</td>
#     <td>CPC Manual Forecast Product</td>
#   </tr>
#   <tr>
#     <td class="center">201</td>
#     <td>CPC Automated Product</td>
#   </tr>
#   <tr>
#     <td class="center">202-209</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">210</td>
#     <td>EPA Air Quality Forecast - Currently Northeast U.S. Domain</td>
#   </tr>
#   <tr>
#     <td class="center">211</td>
#     <td>EPA Air Quality Forecast - Currently Eastern U.S. Domain</td>
#   </tr>
#   <tr>
#     <td class="center">212-214</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">215</td>
#     <td>SPC Manual Forecast Product</td>
#   </tr>
#   <tr>
#     <td class="center">216-219</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">220</td>
#     <td>NCEP/OPC automated product</td>
#   </tr>
#   <tr>
#     <td class="center">221-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 254 (EUMETSAT Operation Centre)</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, with the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Quality values derived from the EUMETSAT QI (Quality Indicator) method, excluding the forecast consistency test</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Quality values derived from the NESDIS RFF (Recursive Filter Function) method</td>
#   </tr>
#   <tr>
#     <td class="center">4-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001033">
# <h4>0-01-033 - OGCE</h4>
# <h4>Identification of originating/generating centre</h4>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>WMO Secretariat</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Melbourne</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>Moscow</td>
#   </tr>
#   <tr>
#     <td class="center">7</td>
#     <td>U.S. National Weather Service, National Centres for Environmental Prediction (NCEP)</td>
#   </tr>
#   <tr>
#     <td class="center">8</td>
#     <td>U.S. National Weather Service Telecommunications Gateway (NWSTG)</td>
#   </tr>
#   <tr>
#     <td class="center">9</td>
#     <td>U.S. National Weather Service - Other</td>
#   </tr>
#   <tr>
#     <td class="center">10</td>
#     <td>Cairo (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">11</td>
#     <td>Cairo (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">12</td>
#     <td>Dakar (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">13</td>
#     <td>Dakar (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">14</td>
#     <td>Nairobi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">15</td>
#     <td>Nairobi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">16</td>
#     <td>Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">17</td>
#     <td>Tunis (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">18</td>
#     <td>Tunis Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">19</td>
#     <td>Tunis Casablanca (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">20</td>
#     <td>Las Palmas</td>
#   </tr>
#   <tr>
#     <td class="center">21</td>
#     <td>Algiers (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">22</td>
#     <td>ACMAD</td>
#   </tr>
#   <tr>
#     <td class="center">23</td>
#     <td>Mozambique (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">24</td>
#     <td>Pretoria (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">25</td>
#     <td>La Réunion (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">26</td>
#     <td>Khabarovsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">27</td>
#     <td>Khabarovsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">28</td>
#     <td>New Delhi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">29</td>
#     <td>New Delhi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">30</td>
#     <td>Novosibirsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">31</td>
#     <td>Novosibirsk (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">32</td>
#     <td>Tashkent (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">33</td>
#     <td>Jeddah (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">34</td>
#     <td>Tokyo (RSMC), Japan Meteorological Agency</td>
#   </tr>
#   <tr>
#     <td class="center">35</td>
#     <td>Tokyo (RSMC), Japan Meteorological Agency</td>
#   </tr>
#   <tr>
#     <td class="center">36</td>
#     <td>Bangkok</td>
#   </tr>
#   <tr>
#     <td class="center">37</td>
#     <td>Ulaanbaatar</td>
#   </tr>
#   <tr>
#     <td class="center">38</td>
#     <td>Beijing (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">39</td>
#     <td>Beijing (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">40</td>
#     <td>Seoul</td>
#   </tr>
#   <tr>
#     <td class="center">41</td>
#     <td>Buenos Aires (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">42</td>
#     <td>Buenos Aires (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">43</td>
#     <td>Brasilia (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">44</td>
#     <td>Brasilia (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">45</td>
#     <td>Santiago</td>
#   </tr>
#   <tr>
#     <td class="center">46</td>
#     <td>Brazilian Space Agency ­ INPE</td>
#   </tr>
#   <tr>
#     <td class="center">47</td>
#     <td>Colombia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">48</td>
#     <td>Ecuador (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">49</td>
#     <td>Peru (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">50</td>
#     <td>Venezuela (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">51</td>
#     <td>Miami (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">52</td>
#     <td>Miami (RSMC), National Hurricane Center</td>
#   </tr>
#   <tr>
#     <td class="center">53</td>
#     <td>MSC Monitoring</td>
#   </tr>
#   <tr>
#     <td class="center">54</td>
#     <td>Montreal (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">55</td>
#     <td>San Francisco</td>
#   </tr>
#   <tr>
#     <td class="center">56</td>
#     <td>ARINC Centre</td>
#   </tr>
#   <tr>
#     <td class="center">57</td>
#     <td>U.S. Air Force Global Weather Central</td>
#   </tr>
#   <tr>
#     <td class="center">58</td>
#     <td>Fleet Numerical Meteorology and Oceanography Center, Monterey, CA, USA</td>
#   </tr>
#   <tr>
#     <td class="center">59</td>
#     <td>NOAA Forecast Systems Laboratory, Boulder, CO, USA</td>
#   </tr>
#   <tr>
#     <td class="center">60</td>
#     <td>United States National Centre for Atmospheric Research (NCAR)</td>
#   </tr>
#   <tr>
#     <td class="center">61</td>
#     <td>Service ARGOS - Landover</td>
#   </tr>
#   <tr>
#     <td class="center">62</td>
#     <td>U.S. Naval Oceanographic Office</td>
#   </tr>
#   <tr>
#     <td class="center">63</td>
#     <td>International Research Institute for Climate and Society (IRI)</td>
#   </tr>
#   <tr>
#     <td class="center">64</td>
#     <td>Honolulu (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">65</td>
#     <td>Darwin (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">66</td>
#     <td>Darwin (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">67</td>
#     <td>Melbourne (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">68</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">69</td>
#     <td>Wellington (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">70</td>
#     <td>Wellington (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">71</td>
#     <td>Nadi (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">72</td>
#     <td>Singapore</td>
#   </tr>
#   <tr>
#     <td class="center">73</td>
#     <td>Malaysia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">74</td>
#     <td>UK Meteorological Office, Exeter (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">75</td>
#     <td>UK Meteorological Office, Exeter (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">76</td>
#     <td>Moscow (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">77</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">78</td>
#     <td>Offenbach (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">79</td>
#     <td>Offenbach (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">80</td>
#     <td>Rome (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">81</td>
#     <td>Rome (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">82</td>
#     <td>Norrköping</td>
#   </tr>
#   <tr>
#     <td class="center">83</td>
#     <td>Norrköping</td>
#   </tr>
#   <tr>
#     <td class="center">84</td>
#     <td>Toulouse (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">85</td>
#     <td>Toulouse (RSMC)</td>
#   </tr>
#   <tr>
#     <td class="center">86</td>
#     <td>Helsinki</td>
#   </tr>
#   <tr>
#     <td class="center">87</td>
#     <td>Belgrade</td>
#   </tr>
#   <tr>
#     <td class="center">88</td>
#     <td>Oslo</td>
#   </tr>
#   <tr>
#     <td class="center">89</td>
#     <td>Prague</td>
#   </tr>
#   <tr>
#     <td class="center">90</td>
#     <td>Episkopi</td>
#   </tr>
#   <tr>
#     <td class="center">91</td>
#     <td>Ankara</td>
#   </tr>
#   <tr>
#     <td class="center">92</td>
#     <td>Frankfurt/Main</td>
#   </tr>
#   <tr>
#     <td class="center">93</td>
#     <td>London (WAFC)</td>
#   </tr>
#   <tr>
#     <td class="center">94</td>
#     <td>Copenhagen</td>
#   </tr>
#   <tr>
#     <td class="center">95</td>
#     <td>Rota</td>
#   </tr>
#   <tr>
#     <td class="center">96</td>
#     <td>Athens</td>
#   </tr>
#   <tr>
#     <td class="center">97</td>
#     <td>European Space Agency (ESA)</td>
#   </tr>
#   <tr>
#     <td class="center">98</td>
#     <td>European Centre for Medium-Range Weather Forecasts (ECMWF)</td>
#   </tr>
#   <tr>
#     <td class="center">99</td>
#     <td>De Bilt</td>
#   </tr>
#   <tr>
#     <td class="center">100</td>
#     <td>Brazzaville</td>
#   </tr>
#   <tr>
#     <td class="center">101</td>
#     <td>Abidjan</td>
#   </tr>
#   <tr>
#     <td class="center">102</td>
#     <td>Libya (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">103</td>
#     <td>Madagascar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">104</td>
#     <td>Mauritius (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">105</td>
#     <td>Niger (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">106</td>
#     <td>Seychelles (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">107</td>
#     <td>Uganda (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">108</td>
#     <td>Tanzania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">109</td>
#     <td>Zimbabwe (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">110</td>
#     <td>Hong-Kong, China</td>
#   </tr>
#   <tr>
#     <td class="center">111</td>
#     <td>Afghanistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">112</td>
#     <td>Bahrain (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">113</td>
#     <td>Bangladesh (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">114</td>
#     <td>Bhutan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">115</td>
#     <td>Cambodia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">116</td>
#     <td>Democratic People's Republic of Korea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">117</td>
#     <td>Islamic Republic of Iran (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">118</td>
#     <td>Iraq (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">119</td>
#     <td>Kazakhstan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">120</td>
#     <td>Kuwait (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">121</td>
#     <td>Kyrgyzstan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">122</td>
#     <td>Lao People's Democratic Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">123</td>
#     <td>Macao, China</td>
#   </tr>
#   <tr>
#     <td class="center">124</td>
#     <td>Maldives (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">125</td>
#     <td>Myanmar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">126</td>
#     <td>Nepal (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">127</td>
#     <td>Oman (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">128</td>
#     <td>Pakistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">129</td>
#     <td>Qatar (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">130</td>
#     <td>Republic of Yemen (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">131</td>
#     <td>Sri Lanka (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">132</td>
#     <td>Tajikistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">133</td>
#     <td>Turkmenistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">134</td>
#     <td>United Arab Emirates (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">135</td>
#     <td>Uzbekistan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">136</td>
#     <td>Viet Nam (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">137-139</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">140</td>
#     <td>Bolivia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">141</td>
#     <td>Guyana (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">142</td>
#     <td>Paraguay (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">143</td>
#     <td>Suriname (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">144</td>
#     <td>Uruguay (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">145</td>
#     <td>French Guyana</td>
#   </tr>
#   <tr>
#     <td class="center">146</td>
#     <td>Brazilian Navy Hydrographic Centre</td>
#   </tr>
#   <tr>
#     <td class="center">147</td>
#     <td>COmision Nacional de Actividades Espaciales (CONAE) - Argentina</td>
#   </tr>
#   <tr>
#     <td class="center">148-149</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">150</td>
#     <td>Antigua and Barbuda (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">151</td>
#     <td>Bahamas (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">152</td>
#     <td>Barbados (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">153</td>
#     <td>Belize (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">154</td>
#     <td>British Caribbean Territories Centre</td>
#   </tr>
#   <tr>
#     <td class="center">155</td>
#     <td>San Jose</td>
#   </tr>
#   <tr>
#     <td class="center">156</td>
#     <td>Cuba (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">157</td>
#     <td>Dominica (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">158</td>
#     <td>Dominican Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">159</td>
#     <td>El Salvador (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">160</td>
#     <td>U.S. NOAA/NESDIS</td>
#   </tr>
#   <tr>
#     <td class="center">161</td>
#     <td>U.S. NOAA Office of Oceanic and Atmospheric Research</td>
#   </tr>
#   <tr>
#     <td class="center">162</td>
#     <td>Guatemala (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">163</td>
#     <td>Haiti (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">164</td>
#     <td>Honduras (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">165</td>
#     <td>Jamaica (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">166</td>
#     <td>Mexico</td>
#   </tr>
#   <tr>
#     <td class="center">167</td>
#     <td>Curaçao and Sint Maarten (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">168</td>
#     <td>Nicaragua (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">169</td>
#     <td>Panama (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">170</td>
#     <td>Saint Lucia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">171</td>
#     <td>Trinidad and Tobago (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">172</td>
#     <td>French Departments in RA IV</td>
#   </tr>
#   <tr>
#     <td class="center">173</td>
#     <td>U.S. National Aeronautics and Space Administration (NASA)</td>
#   </tr>
#   <tr>
#     <td class="center">174</td>
#     <td>Integrated System Data Management/Marine Environmental Data Service (ISDM/MEDS - Canada)</td>
#   </tr>
#   <tr>
#     <td class="center">175</td>
#     <td>University Corporation for Atmospheric Research (UCAR) - United States</td>
#   </tr>
#   <tr>
#     <td class="center">176</td>
#     <td>U.S. Cooperative Institute for Meteorological Satellite Studies (CIMSS)</td>
#   </tr>
#   <tr>
#     <td class="center">177</td>
#     <td>U.S. NOAA National Ocean Service</td>
#   </tr>
#   <tr>
#     <td class="center">178</td>
#     <td>Spire Global, Inc.</td>
#   </tr>
#   <tr>
#     <td class="center">179-189</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">190</td>
#     <td>Cook Islands (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">191</td>
#     <td>French Polynesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">192</td>
#     <td>Tonga (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">193</td>
#     <td>Vanuatu (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">194</td>
#     <td>Brunei Darussalam (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">195</td>
#     <td>Indonesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">196</td>
#     <td>Kiribati (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">197</td>
#     <td>Federated States of Micronesia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">198</td>
#     <td>New Caledonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">199</td>
#     <td>Niue</td>
#   </tr>
#   <tr>
#     <td class="center">200</td>
#     <td>Papua New Guinea (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">201</td>
#     <td>Philippines (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">202</td>
#     <td>Samoa (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">203</td>
#     <td>Solomon Islands (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">204</td>
#     <td>National Institute of Water and Atmospheric Research  (NIWA – New Zealand)</td>
#   </tr>
#   <tr>
#     <td class="center">205-209</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">210</td>
#     <td>Frascati (ESA/ESRIN)</td>
#   </tr>
#   <tr>
#     <td class="center">211</td>
#     <td>Lannion</td>
#   </tr>
#   <tr>
#     <td class="center">212</td>
#     <td>Lisboa</td>
#   </tr>
#   <tr>
#     <td class="center">213</td>
#     <td>Reykiavik</td>
#   </tr>
#   <tr>
#     <td class="center">214</td>
#     <td>Madrid</td>
#   </tr>
#   <tr>
#     <td class="center">215</td>
#     <td>Zürich</td>
#   </tr>
#   <tr>
#     <td class="center">216</td>
#     <td>Service ARGOS Toulouse</td>
#   </tr>
#   <tr>
#     <td class="center">217</td>
#     <td>Bratislava</td>
#   </tr>
#   <tr>
#     <td class="center">218</td>
#     <td>Budapest</td>
#   </tr>
#   <tr>
#     <td class="center">219</td>
#     <td>Ljubljana</td>
#   </tr>
#   <tr>
#     <td class="center">220</td>
#     <td>Warsaw</td>
#   </tr>
#   <tr>
#     <td class="center">221</td>
#     <td>Zagreb</td>
#   </tr>
#   <tr>
#     <td class="center">222</td>
#     <td>Albania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">223</td>
#     <td>Armenia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">224</td>
#     <td>Austria (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">225</td>
#     <td>Azerbaijan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">226</td>
#     <td>Belarus (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">227</td>
#     <td>Belgium (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">228</td>
#     <td>Bosnia and Herzegovina (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">229</td>
#     <td>Bulgaria (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">230</td>
#     <td>Cyprus (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">231</td>
#     <td>Estonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">232</td>
#     <td>Georgia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">233</td>
#     <td>Dublin</td>
#   </tr>
#   <tr>
#     <td class="center">234</td>
#     <td>Israel (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">235</td>
#     <td>Jordan (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">236</td>
#     <td>Latvia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">237</td>
#     <td>Lebanon (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">238</td>
#     <td>Lithuania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">239</td>
#     <td>Luxembourg</td>
#   </tr>
#   <tr>
#     <td class="center">240</td>
#     <td>Malta (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">241</td>
#     <td>Monaco</td>
#   </tr>
#   <tr>
#     <td class="center">242</td>
#     <td>Romania (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">243</td>
#     <td>Syrian Arab Republic (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">244</td>
#     <td>The former Yugoslav Republic of Macedonia (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">245</td>
#     <td>Ukraine (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">246</td>
#     <td>Republic of Moldova (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">247</td>
#     <td>Operational Programme for the Exchange of weather RAdar information (OPERA) - EUMETNET</td>
#   </tr>
#   <tr>
#     <td class="center">248</td>
#     <td>Montenegro (NMC)</td>
#   </tr>
#   <tr>
#     <td class="center">249</td>
#     <td>Barcelona Dust Forecast Center</td>
#   </tr>
#   <tr>
#     <td class="center">250</td>
#     <td>COnsortium for Small scale MOdelling  (COSMO)</td>
#   </tr>
#   <tr>
#     <td class="center">251</td>
#     <td>Meteorological Cooperation on Operational NWP (MetCoOp)</td>
#   </tr>
#   <tr>
#     <td class="center">252</td>
#     <td>Max Planck Institute for Meteorology (MPI-M)</td>
#   </tr>
#   <tr>
#     <td class="center">253</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">254</td>
#     <td>EUMETSAT Operation Centre</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <hr id="001034">
# <h4>0-01-034 - GSES</h4>
# <h4>Identification of originating/generating sub-centre</h4>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 2 (Melbourne)</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No sub-centre</td>
#   </tr>
#   <tr>
#     <td class="center">1-200</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">201</td>
#     <td>Casey</td>
#   </tr>
#   <tr>
#     <td class="center">202</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">203</td>
#     <td>Davis</td>
#   </tr>
#   <tr>
#     <td class="center">204-209</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">210</td>
#     <td>Alice Springs</td>
#   </tr>
#   <tr>
#     <td class="center">211</td>
#     <td>Melbourne Crib Point 1</td>
#   </tr>
#   <tr>
#     <td class="center">212-213</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">214</td>
#     <td>Darwin</td>
#   </tr>
#   <tr>
#     <td class="center">215-216</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">217</td>
#     <td>Perth</td>
#   </tr>
#   <tr>
#     <td class="center">218</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">219</td>
#     <td>Townsville</td>
#   </tr>
#   <tr>
#     <td class="center">220-231</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">232</td>
#     <td>Fiji</td>
#   </tr>
#   <tr>
#     <td class="center">233-234</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">235</td>
#     <td>Noumea</td>
#   </tr>
#   <tr>
#     <td class="center">236</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">237</td>
#     <td>Papeete</td>
#   </tr>
#   <tr>
#     <td class="center">238-249</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">250</td>
#     <td>Vladivostock</td>
#   </tr>
#   <tr>
#     <td class="center">251</td>
#     <td>Guam</td>
#   </tr>
#   <tr>
#     <td class="center">252</td>
#     <td>Honolulu</td>
#   </tr>
#   <tr>
#     <td class="center">253-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 160 (U.S. NOAA/NESDIS)</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No sub-centre</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>National Climatic Data Center</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>National Geophysical Data Center</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>National Oceanographic Data Center</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>Center for Satellite Applications and Research (STAR)</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Joint Polar Satellite System</td>
#   </tr>
#   <tr>
#     <td class="center">6-9</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">10</td>
#     <td>Tromso (Norway)</td>
#   </tr>
#   <tr>
#     <td class="center">11</td>
#     <td>McMurdo (Antarctica)</td>
#   </tr>
#   <tr>
#     <td class="center">12-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 173 (U.S. National Aeronautics and Space Administration (NASA))</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No sub-centre</td>
#   </tr>
#   <tr>
#     <td class="center">1</td>
#     <td>Ames Research Center</td>
#   </tr>
#   <tr>
#     <td class="center">2</td>
#     <td>Dryden Flight Research Center</td>
#   </tr>
#   <tr>
#     <td class="center">3</td>
#     <td>Glenn Research Center</td>
#   </tr>
#   <tr>
#     <td class="center">4</td>
#     <td>Goddard Space Flight Center</td>
#   </tr>
#   <tr>
#     <td class="center">5</td>
#     <td>Jet Propulsion Laboratory</td>
#   </tr>
#   <tr>
#     <td class="center">6</td>
#     <td>Johnson Space Center</td>
#   </tr>
#   <tr>
#     <td class="center">7</td>
#     <td>Kennedy Space Center</td>
#   </tr>
#   <tr>
#     <td class="center">8</td>
#     <td>Langley Research Center</td>
#   </tr>
#   <tr>
#     <td class="center">9</td>
#     <td>Marshall Space Flight Center</td>
#   </tr>
#   <tr>
#     <td class="center">10</td>
#     <td>Stennis Space Center</td>
#   </tr>
#   <tr>
#     <td class="center">11</td>
#     <td>Goddard Institute for Space Studies</td>
#   </tr>
#   <tr>
#     <td class="center">12</td>
#     <td>Independent Verification and Validation Facility</td>
#   </tr>
#   <tr>
#     <td class="center">13</td>
#     <td>NASA Shared Service Center</td>
#   </tr>
#   <tr>
#     <td class="center">14</td>
#     <td>Wallops Flight Facility</td>
#   </tr>
#   <tr>
#     <td class="center">15-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
# <br />
# <p class="left">When the value of<br>
# <span class="bold indent">0-01-031 - GCLONG (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-033 - OGCE (Identification of originating/generating centre)</span><br>
# <span class="indentX2">or</span><br>
# <span class="bold indent">0-01-035 - ORIGC (Originating centre)<br><br>
# = 69 (Wellington (RSMC))</span></p>
# <table rules=groups>
#  <thead>
#   <tr>
#     <th>Code figure</th>
#     <th class="left">Meaning</th>
#   </tr>
#  </thead>
#  <tbody>
#   <tr>
#     <td class="center">0</td>
#     <td>No sub-centre</td>
#   </tr>
#   <tr>
#     <td class="center">1-203</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">204</td>
#     <td>National Institute of Water and Atmospheric Research (NIWA - New Zealand)</td>
#   </tr>
#   <tr>
#     <td class="center">205</td>
#     <td>Niue</td>
#   </tr>
#   <tr>
#     <td class="center">206</td>
#     <td>Raotonga (Cook Islands)</td>
#   </tr>
#   <tr>
#     <td class="center">207</td>
#     <td>Apia (Samoa)</td>
#   </tr>
#   <tr>
#     <td class="center">208</td>
#     <td>Tonga</td>
#   </tr>
#   <tr>
#     <td class="center">209</td>
#     <td>Tuvalu</td>
#   </tr>
#   <tr>
#     <td class="center">210</td>
#     <td>Kiribati</td>
#   </tr>
#   <tr>
#     <td class="center">211</td>
#     <td>Tokelau</td>
#   </tr>
#   <tr>
#     <td class="center">212-242</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">243</td>
#     <td>Kelburn</td>
#   </tr>
#   <tr>
#     <td class="center">244-254</td>
#     <td>Reserved</td>
#   </tr>
#   <tr>
#     <td class="center">255</td>
#     <td>Missing value</td>
#   </tr>
#  </tbody>
# </table>
"""


# data_dict = parse_html_table_b_x_entries(html_table)
# for ikey in data_dict.keys():
  # print(f'"{ikey}": ' + str(data_dict[ikey]) + ",")

# data_dict = parse_html_table_d_x(html_table)
# for ikey in data_dict.keys():
#   print(f'{ikey}: "' + str(data_dict[ikey]) + "\",")

# data_dict = parse_html_table_d_x_entries(html_table)
# # for ikey in data_dict.keys():
# #   print(f'"{ikey}": ' + str(data_dict[ikey]) + ",")
# pprint(data_dict, width=110, compact=True)

data_dict = parse_html_table_code_figure(html_table)
pprint(data_dict, width=110, compact=True)

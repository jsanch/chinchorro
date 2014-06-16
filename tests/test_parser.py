import random
import unittest
from modules import parser,url_generator
from bs4 import BeautifulSoup,SoupStrainer
from classes.Documento import Documento
from decimal import Decimal
from datetime import datetime
import urllib3

conn = urllib3.HTTPConnectionPool('190.34.178.19', maxsize=15)
url = '/Sicowebconsultas/buscar.aspx'

data = url_generator.parse_har()
html = conn.request("POST", url, data).data.decode('ISO-8859-1','ignore')
soup = BeautifulSoup(html,'lxml')

data_with_pages = url_generator.set_document_id(data,'_')
html_with_pages = conn.request("POST", url, data_with_pages).data.decode('ISO-8859-1','ignore')

#print(html_with_pages)
soup_with_pages = BeautifulSoup(html_with_pages,'lxml')
office_ids = [202, 43, 624, 108, 1, 29, 114, 238, 234, 105, 47, 145, 22, 103, 203, 107, 109, 16015, 106, 55, 57, 204, 315, 330, 345, 600, 115, 208, 11018, 274, 360, 110, 212, 375, 521, 522, 311, 11004, 11014, 625, 623, 628, 58, 45, 611, 614, 612, 613, 615, 616, 617, 618, 610, 619, 31, 2, 53, 224, 621, 1702, 33, 111, 11005, 11006, 49, 41, 397, 63, 50, 60, 1703, 299, 704, 900, 198, 278, 699, 54, 701, 38, 39, 123, 52, 11015, 1232, 118, 124, 152, 266, 120, 137, 51, 125, 391, 362, 270, 390, 130, 392, 23, 122, 151, 142, 140, 640, 643, 644, 639, 645, 641, 646, 642, 622, 638, 649, 635, 653, 652, 650, 647, 632, 636, 651, 633, 637, 648, 634, 620, 282, 163, 16501, 10091, 8, 10, 21, 16, 7, 7041, 7061, 17, 3, 9, 12, 12021, 18, 13, 14, 20, 5, 629, 507, 525, 508, 569, 585, 570, 526, 541, 501, 527, 528, 529, 586, 587, 571, 597, 517, 572, 502, 543, 573, 574, 503, 547, 516, 580, 530, 531, 518, 532, 558, 524, 539, 545, 575, 588, 509, 548, 589, 559, 549, 560, 561, 584, 538, 590, 542, 510, 540, 546, 550, 511, 576, 551, 562, 512, 552, 544, 563, 519, 533, 534, 591, 596, 577, 535, 592, 536, 578, 593, 520, 553, 594, 595, 579, 537, 564, 146, 700, 28, 30, 135, 117, 37, 800, 999, 11003, 181, 11011, 11008, 11009, 11010, 11012, 11007, 153, 11002, 133, 36, 1619, 35, 1633, 148, 11, 703, 44, 134, 705, 226, 276, 56, 112, 183, 119, 182, 184, 27, 1701, 655, 310, 121, 275, 26, 626, 702, 40, 193, 187, 190, 46, 195, 100, 296]

doc_types = ['AC', 'ACO', 'ACUE', 'ACUEM', 'AJOC', 'CASER', 'CAT', 'CCR', 'CCUE', 'CD', 'CDNO', 'CEFA', 'CEFOIN', 'CF', 'CH', 'CHEC', 'CHESB', 'CHI', 'CO', 'COMPP', 'CONV', 'CPA', 'CUE', 'CUEP', 'CUET', 'DEM', 'DEN', 'DJB', 'ENM', 'GC', 'GCOSB', 'LETT', 'LEVE', 'LEVP', 'LEVS', 'LEYTRANSP', 'LIQ', 'MOV', 'OC', 'OF', 'OP', 'PAC', 'PAL', 'PLANAD', 'PLANCOM', 'POD', 'POL', 'QUE', 'RC', 'REC', 'REDPART', 'REEM', 'REEMPRE', 'REISO', 'RES', 'RF', 'RPA', 'SAD', 'SOL', 'SV', 'TRA', 'TRA.CERP', 'TRAS']

event_val = '/wEW5wICtbDCiA8C6e6JxwgCgtHVZgKOkrn2CAL0kfHzAwKgotqqAQLjz46BDQKupPLxAwLtqcvFDAL57+62CwKR7recBwKp6fXRAwLuwt+tDQKqgv6VAwLup86DDQLXj+6SDwLup96LDgK+kaLvAgLkx765DALl4L65DALYh56KDgKS5q/YBwKDzZGADgKTybm0AwLur9qvDwLYj+o2AqqC6q0CAtC4yqcOAre6nogBAtC43osOArrkiiAC7qfKpw4C7sLLxQwCjaaihggCq4LOnQQCuLri7AICtamWxAECoKKmzwIC0biicAL+iff6DAKjq6LvAgL8+OraDAKJpda7CwKJpaKGCALT4tbHDgLpgof9DQLS5NOJDALtsaf2DgLtr96LDgL/ouvaDAKupPbRAwKkxKbPAgLpgrvdDQLT4sqnDgKYhIbYBALdwpquDwLS5NfpDQK65JbEAQKXobT8CAL57/KeDAK+kdqqAQLkz4qlDgKqgvLxAwL/ovf6DALlitqdCQLjz4LhDgL65+raDALopta7CwLHpda7CwKR7r+gCAL57/6+DALamLrYDQLkz5bFDgK1sebMAgK1seLsAgKGitqdCQKT/8vpBgKvnOqtAgKN5IkgAu2p95sKAu/Cr7oOApeh1OkGAqnxxdkEAuCa77YLAuyx360NApHus4AIAuTHhv0NAr+RttcDAuimooYIAsyM2ogIAu2p1+kNAqnp8fEDAqCJttcDApXikcAFArWpkuQBAtiH4nIC+u/6og0C7qfWxw4C/PiKxAoCktG10A4Ct8LukAICt7q29g8CtameiAECoZrGeALjz4b9DQK/iaLvAgL75/qiDQK/iaqzAgK1qZqoAQK65JqoAQLpgo+BDQKupPq1AwKXobyACALT4t6LDgL/ov++DAKYhIq8BAKkxKqzAgKkxKLvAgLS5N+tDQKXobigCALT4tLrDwLqgoulDgKlxLbXAwK75ObMAgLdwu6SDwKkxK6TAgKYhI6cBALgovuiDQLpgoPhDgLdwuJyAtLk280NAq6k/pUDArrkkuQBAqCi+tQPApLRuZoKAuLNrYsJAq2vkqgLAuyxy8UMArSxlsQBAvnv9voMApLRhdgEAtePnooOAquLkugJAumLkugJAtePmq4PAuPPvrkMApHur9gHAr6Rps8CAsyMorMMAuyx1+kNAuPPut0NAqjx9dEDArSxkuQBAu2vzoMNApehsJwHAtypnooOAtLJ1scOAtHLy8UMApeIgOQJAtLJ7q0LArrL7pACApfrgfgEAv6J/74MAv6J77YLAtyp5s4PAtHL04kMApaIsJwHApfr2aEBAtypvrQMAv+Jw+YOAtyputgNAtypmq4PAqSrvpsDAqOr2qoBAujpjoENAunpkukPAq6Lzp0EAujpvrkMAtyp7pIPApfrhdgEArnLqtIOArnLnogBAv6J854MAtHL1+kNAqOrrpMCAtLLp/YOAq2L8vEDApaIvIAIAtLJ3osOAtPJonAC0cvr9woCloio2AcC0cvbzQ0ClojIxQUCl4iExAkCloi4oAgCusvi7AIC/4nHwg0CrYuKXwLRy9+tDQK5y7b2DwKjq6qzAgK5y5bEAQK5y5qoAQKX64m8BAK6y+bMAgL+ievaDAKY653kBgL/ifuiDQKkq7L3AwKjq6bPAgKkq7bXAwKti/q1AwLp6ZbFDgKWiLT8CALo6YLhDgKti/6VAwL+iYvECgKX66XKAgLdqfL6AQLSydLrDwKjq8Z4ApfrjZwEAtLLr7oOAujp2s4LArnLkuQBAunpiqUOAq2LlsMBAtLJ6tEMApeIjIgJAtyp4nICrovC+QQCk8mJvAQCu9yKIALssdOJDAK0sZ6IAQLup9LrDwLYh5quDwLXj+JyAozsiSAC6qLL6QYCoqTWuwsC7LHjqwQC5KWihggCjabWuwsC7KfWuwsChaSihggCw6SihggCpqXWuwsC5ceKpQ4Cw6TWuwsC5MeC4Q4CktGNnAQCi8/RlQsC48+a+wICwc25mgoC7anbzQ0C+e/q2gwC6vq+uQwCqPH5tQMCqen9lQMC1NrOgw0ClOKB+AQCleKd5AYCk9GVoAUCv4mmzwIC7LHLqwMCkuar/AgC7LH/3QYC7LGnogUC14/mzg8CyIvanQkC1OLarw8Ct7qWxAEC+uf2+gwC0MCicAKS0YH4BAKYhIL4BAKlvNqqAQK0sZqoAQLkx9rOCwLYh760DAK1qbb2DwKS0Ym8BALup+rRDAK1qYogApTipcoCAsepkfcHAuOopekHAtKj6p0PAtyP+KsLAveFpY4HAtKjgqQMAvCp0fcMAv+YqoIPArHK9ekEAuKP+KsLAuGooekHAu28+I0LApWCvZELAuT6uroGAuGoqekHAuGo8ekHArKbz6UPAv6TtEYC9qrxnAwC4aiV6QcC4M36pg8C7byw0AUCnvDitgMCspuHnQoCspvHmQECspuXjQwCidW1wwQC7LyQ9gICgOf03QkCiNWRwwQC5ail6QcCoJuLzQUC9pjKswECvPXi3gECvPXG2AoCvPX6qQwCz/n/4AkCxeTjwg4Cw/bu3AMC3ail6QcC3aip6QcC3ajR6QcC4bKm9woCku673A4C9vOHgAgCv7+TiAUCurTN9w0Cku6z3A4CnJuHnQoC0qil6QcC1c76wAcC99bkwQQCo5uDxgMCsOKD8wMClqzOywoChbHYnAEC0qip6QcCj/DitgMCv7TV9w0Cl+6z3A4C0ajp6QcCjfDqtgMC7PWJoQECjfDugwwCsr6DXALSzMHkDAKfo/csAq7zvMoBAtOOkcwPAvyYk8wPApnhncwPArrnjswP2eodl9blOqIVHgMBLP2k2dhI0n0='

class TestParser(unittest.TestCase):

    def test_get_office_ids(self):
        ids = parser.get_office_ids(soup)
        self.assertEqual(ids,office_ids)

    def test_get_event_validation(self):
        ev = parser.get_event_validation(soup)
        self.assertEqual(ev,event_val)

    def test_get_documento_types(self):
        ids = parser.get_documento_types(soup)
        self.assertEqual(ids,doc_types)

    def test_has_pages(self):
        self.assertFalse(parser.has_pages(soup))
        self.assertTrue(parser.has_pages(soup_with_pages))

    def test_get_documentos(self):
        docs = parser.get_documentos(soup_with_pages)
        self.assertTrue(isinstance(docs,list))
        for d in docs:
            self.assertTrue(isinstance(d,Documento))
        self.assertEqual(len(docs),20)

    def test_get_documento_control(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.control,'0-03-5-111917-7638445')

    def test_get_documento_institucion(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.institucion,'PROGRAMA DE AYUDA NACIONAL')

    def test_get_documento_type(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.documento,'ORDEN DE COMPRA')

    def test_get_documento_numero(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.numero,'57679')

    def test_get_documento_favor(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.favor,'GEO MEDIA, S.A.')

    def test_get_documento_estado(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.estado,'En Subsanación')

    def test_get_documento_fecha(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(d.fecha,datetime(2013, 1, 9, 12, 31))

    def test_get_documento_monto(self):
        docs = parser.get_documentos(soup)
        d = docs[0]
        self.assertEqual(float(d.monto),float(612.04))

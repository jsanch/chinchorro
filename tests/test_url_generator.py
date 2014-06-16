import unittest
from modules import url_generator
import urllib.parse
from time import sleep

class TestUrlGenerator(unittest.TestCase):
    def setUp(self):
        self.har = url_generator.parse_har()

    def test_get_document_id(self):
        doc_id = url_generator.get_document_id(self.har)
        self.assertEqual(doc_id,'57___')

    def test_get_oficina_id(self):
        ofi_id = url_generator.get_oficina_id(self.har)
        self.assertEqual(ofi_id,'0035')

    def test_get_year(self):
        year = url_generator.get_year(self.har)
        self.assertEqual(year,2013)

    def test_set_year(self):
        data = url_generator.set_year(self.har,2014)
        year = url_generator.get_year(data)
        self.assertEqual(year,2014)

    def test_set_oficina_id(self):
        data = url_generator.set_oficina_id(self.har,'134')
        oficina_id = url_generator.get_oficina_id(data)
        self.assertEqual(oficina_id,'134')

    def test_set_document_id(self):
        data = url_generator.set_document_id(self.har,'_')
        document_id = url_generator.get_document_id(data)
        self.assertEqual(document_id,'_')

    def test_get_page(self):
        page = url_generator.get_page(self.har)
        self.assertEqual(page,1)

    def test_increment_page(self):
        page = url_generator.get_page(self.har)
        data = url_generator.increment_page(self.har)
        page2 = url_generator.get_page(data)
        data = url_generator.increment_page(self.har)
        page3 = url_generator.get_page(data)
        self.assertEqual(page+1,page2,page3-1)

    def test_get_doc_type(self):
        doc_type = url_generator.get_doc_type(self.har)
        self.assertEqual(doc_type,'OC')

    def test_set_doc_type(self):
        data = url_generator.set_doc_type(self.har,'FF')
        doc_type = url_generator.get_doc_type(data)
        self.assertEqual(doc_type,'FF')

    def test_generate_document_space(self):
        documents = url_generator.generate_data_for_office_and_year(self.har,'111',2014)
        for i,doc in enumerate(documents):
                oficina_id = url_generator.get_oficina_id(doc)
                doc_id = url_generator.get_document_id(doc)
                year = url_generator.get_year(doc)
                self.assertEqual(doc_id,i)
                self.assertEqual(oficina_id,'111')
                self.assertEqual(year,2014)

    def test_generate_document_space_all_years(self):
        '''incomplete test'''
        documents = url_generator.generate_data_for_office(self.har,'111')
        for i,doc in enumerate(documents):
                oficina_id = url_generator.get_oficina_id(doc)
                doc_id = url_generator.get_document_id(doc)
                year = url_generator.get_year(doc)
                self.assertEqual(oficina_id,'111')


if __name__ == '__main__':
    unittest.main()


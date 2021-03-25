from netology.unit_test_s.app import (check_document_existance, get_doc_owner_name, get_all_doc_owners_names,
                                      show_all_docs_info, get_doc_shelf, add_new_doc, delete_doc, move_doc_to_shelf,
                                      add_new_shelf
                                      )


class TestClass:
    # def setup(self):
    #     print("method setup")

    # def teardown(self):
    #     print("method teardown")

    def test_check_document_existance_11(self):
        assert check_document_existance('10006') == True

    def test_check_document_existance_21(self):
        assert check_document_existance('100063') == False

    def test_get_doc_owner_name_11(self, monkeypatch):
        test_input = '10006'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert get_doc_owner_name() == 'Аристарх Павлов'

    def test_get_doc_owner_name_21(self, monkeypatch):
        test_input = '100063'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert get_doc_owner_name() == None

    def test_get_all_doc_owners_names_11(self):
        assert get_all_doc_owners_names() == {'Аристарх Павлов', 'Василий Гупкин', 'Геннадий Покемонов'}

    def test_show_all_docs_info_11(self):
        assert show_all_docs_info() == ['passport "2207 876234" "Василий Гупкин"',
                                        'invoice "11-2" "Геннадий Покемонов"',
                                        'insurance "10006" "Аристарх Павлов"'
                                        ]

    def test_get_doc_shelf_11(self, monkeypatch):
        test_input = '10006'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert get_doc_shelf() == '2'

    def test_get_doc_shelf_21(self, monkeypatch):
        test_input = '100063'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert get_doc_shelf() == None

    def test_add_new_doc_11(self, monkeypatch):
        def inp_generator():
            test_input = ['12345', 'ticket', 'test_user_name', '3']
            for el in test_input:
                yield el

        input_generator = iter(inp_generator())
        monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
        assert add_new_doc, delete_doc() == '3'

    def test_delete_doc_11(self, monkeypatch):
        test_input = '10006'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert delete_doc() == ('10006', True)

    def test_move_doc_to_shelf_11(self, monkeypatch):
        def inp_generator():
            test_input = ['10006', '3']
            for el in test_input:
                yield el

        input_generator = iter(inp_generator())
        monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
        assert move_doc_to_shelf() == 'Документ номер "10006" был перемещен на полку номер "3"'

    def test_add_new_shelf_11(self, monkeypatch):
        test_input = '4'
        monkeypatch.setattr('builtins.input', lambda _: test_input)
        assert add_new_shelf() == ('4', True)

from netology.unit_test_s.ya_disk_api import ya_disk_create_folder, ya_disk_delete_folder


class TestClass:

    def test_ya_disk_create_folder_11(self):
        r_code, r_json = ya_disk_create_folder('test_folder')
        assert r_code == 201

    def test_ya_disk_create_folder_21(self):
        r_code, r_json = ya_disk_create_folder('test_folder')
        assert r_code == 409

    def test_ya_disk_delete_folder_11(self):
        r_code, r_json = ya_disk_delete_folder('test_folder')
        assert r_code == 204

    def test_ya_disk_delete_folder_21(self):
        r_code, r_json = ya_disk_delete_folder('test_folder')
        assert r_code == 404
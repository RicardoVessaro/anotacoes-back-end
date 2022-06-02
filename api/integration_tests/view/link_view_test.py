
from arq.util.test.view.arq_view_test import FindFilterResult, PaginateFilterResult
from arq.util.test.view.detail_crud_view_test import DetailCRUDViewTest
from api.annotation.view.link_view import LinkView

class TestLinkView(DetailCRUDViewTest):

    view = LinkView()    

    filter_to_not_found = {"title": "to not found"}

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"title":"Link 1"}, expected_indexes=[1]),
        FindFilterResult(filter={"title":["Link 1", "Link 2" ] }, expected_indexes=[1,2]),
        FindFilterResult(filter={"title":"Link 4"}, expected_indexes=[]),
        FindFilterResult(filter={"href":"www.link1.com"}, expected_indexes=[1]),
        FindFilterResult(filter={"href":["www.link1.com", "www.link2.com" ] }, expected_indexes=[1,2]),
        FindFilterResult(filter={"href":"www.link4.com"}, expected_indexes=[])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(8,13), pages=2, page=1, limit=5, total=7, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":2}, expected_indexes=range(13,15), pages=2, page=2, limit=5, total=7, has_prev=True, has_next=False, has_result=True),
        PaginateFilterResult(filter={"title":"Link 9"}, expected_indexes=[9], pages=1, page=1, limit=5, total=1, has_prev=False, has_next=False, has_result=True),
        PaginateFilterResult(filter={"title":["Link 10", "Link 11"]}, expected_indexes=[10, 11], pages=1, page=1, limit=5, total=2, has_prev=False, has_next=False, has_result=True),
        PaginateFilterResult(filter={"href":"www.link9.com"}, expected_indexes=[9], pages=1, page=1, limit=5, total=1, has_prev=False, has_next=False, has_result=True),
        PaginateFilterResult(filter={"href":["www.link10.com", "www.link11.com"]}, expected_indexes=[10, 11], pages=1, page=1, limit=5, total=2, has_prev=False, has_next=False, has_result=True)
    ]


    def get_model(self):
        return self.model(
            title='Test Link',
            href='www.test-link.com',
            note_id=self.fake_parent_id
        )

    def get_parent_model(self):
        return self.parent_dao.model(
            id=self.fake_parent_id,
            title="test",
            pinned=False,
            text="lorem ipsum dolor sit amet",
        )

    def get_updated_model(self):
        return self.model(
            title='Updated Test Link',
            href='www.updated-test-link.com',
            note_id=self.fake_parent_id
        )

    def find_model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(6):

            parent_id = self.fake_parent_id
            if i > 2:
                parent_id = other_parent_id

            db_model = self.model(
                title=f'Link {i}',
                href=f'www.link{i}.com',
                note_id=parent_id
            )

            model_list.append(db_model)

        return model_list

    def paginate_model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(15):

            parent_id = self.fake_parent_id
            if i < 8:
                parent_id = other_parent_id

            db_model = self.model(
                title=f'Link {i}',
                href=f'www.link{i}.com',
                note_id=parent_id
            )

            model_list.append(db_model)

        return model_list

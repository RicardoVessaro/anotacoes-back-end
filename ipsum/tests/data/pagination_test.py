
from pytest import raises
from ipsum.exception.exception_message import PAGINATION_OFFSET_GREATER_THAN_TOTAL
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.util.data.pagination import Pagination


class TestPagination:

    def test_build(self):

        def _with_offset_0_limit_5():
            results_size = 20

            expected_items = self._get_results(0, 5)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 0,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size)
            )

            assert expected == pagination.build()

        _with_offset_0_limit_5()

        def _with_offset_5_limit_5():
            results_size = 20

            expected_items = self._get_results(5, 10)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 5,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=5
            )

            assert expected == pagination.build()

        _with_offset_5_limit_5()

        def _with_offset_10_limit_5():
            results_size = 20

            expected_items = self._get_results(10, 15)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 10,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=10
            )

            assert expected == pagination.build()
        _with_offset_10_limit_5()

        def _with_offset_15_limit_5():
            results_size = 20

            expected_items = self._get_results(15, 20)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 15,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=15
            )

            assert expected == pagination.build()

        _with_offset_15_limit_5()

        def _with_offset_0_limit_7():
            results_size = 28

            expected_items = self._get_results(0, 7)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 0,
                    Pagination.LIMIT: 7,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=0,
                limit=7
            )

            assert expected == pagination.build()

        _with_offset_0_limit_7()

        def _with_offset_7_limit_7():
            results_size = 28

            expected_items = self._get_results(7, 14)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 7,
                    Pagination.LIMIT: 7,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=7,
                limit=7
            )

            assert expected == pagination.build()

        _with_offset_7_limit_7()

        def _with_offset_14_limit_7():
            results_size = 28

            expected_items = self._get_results(14, 21)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 14,
                    Pagination.LIMIT: 7,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=14,
                limit=7
            )

            assert expected == pagination.build()

        _with_offset_14_limit_7()

        def _with_offset_21_limit_7():
            results_size = 28

            expected_items = self._get_results(21, 28)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 21,
                    Pagination.LIMIT: 7,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=21,
                limit=7
            )

            assert expected == pagination.build()

        _with_offset_21_limit_7()

    def test_build_bounds(self):

        def _with_3_results_limit_5():
            results_size = 3

            expected_items = self._get_results(0, 3)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 0,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=0,
                limit=5
            )

            assert expected == pagination.build()
        
        _with_3_results_limit_5()

        def _with_7_results_offset_4_limit_5():
            results_size = 7

            expected_items = self._get_results(4, 7)
            expected = {
                Pagination.ITEMS: expected_items,
                Pagination.INFO: {
                    Pagination.OFFSET: 4,
                    Pagination.LIMIT: 5,
                    Pagination.TOTAL: results_size,
                    Pagination.EMPTY: False
                }
            }

            pagination = Pagination(
                results=self._get_results(0, results_size),
                offset=4,
                limit=5
            )

            assert expected == pagination.build()

        _with_7_results_offset_4_limit_5()

    def test_with_empty_result(self):
        results_size = 0

        expected_items = []
        expected = {
            Pagination.ITEMS: expected_items,
            Pagination.INFO: {
                Pagination.OFFSET: 4,
                Pagination.LIMIT: 5,
                Pagination.TOTAL: results_size,
                Pagination.EMPTY: True
            }
        }

        pagination = Pagination(
            results=None,
            offset=4,
            limit=5
        )

        assert expected == pagination.build()

    def test_must_raise_exception_when_offset_is_greater_than_total(self):
        pagination = Pagination(
            results=self._get_results(0, 15),
            offset=15,
            limit=5
        )

        with raises(IpsumException, match=PAGINATION_OFFSET_GREATER_THAN_TOTAL.format(Pagination.OFFSET, 15, Pagination.TOTAL, 14)):
            pagination.build()


    def _get_results(self, start, end):
        return list(range(start, end))
# -*- coding: utf-8 -*-

from audinota import api


def test():
    _ = api


if __name__ == "__main__":
    from audinota.tests import run_cov_test

    run_cov_test(
        __file__,
        "audinota.api",
        preview=False,
    )

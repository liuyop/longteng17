from datetime import datetime
import os


# def pytest_configure(config):
#     now = datetime.now().strftime("%Y%m%d_%H%M%S")
#     config.option.htmlpath = os.path.join(
#         config.rootdir, 'reports', f'report_{now}.html')
#
#     config.option.log_file = os.path.join(
#         config.rootdir, 'reports', f'pytest_{now}.log')
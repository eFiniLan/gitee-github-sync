gitee-github-sync
------
A small python script for clicking the "sync" button on the gitee repository page with selenium.

This script was last tested on **2019/06/19**

```bash
git clone https://github.com/efiniLan/gitee-github-sync.git
sudo apt-get install python-pip
sudo pip install selenium
# download geckodriver (https://github.com/mozilla/geckodriver/releases) if necessary
cd gitee-github-sync
python gitee-github-sync.py <gitee_username> <gitee_password>
```
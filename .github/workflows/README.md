# GITHUB CI/CD
uses: actions/setup-python@v2
Это использование сторонних actions для разных целей, в данном случае для установки Python. Используется официальный репозиторий "actions"

uses: actions/checkout@v2
Это клонирование репозитория в билд-машину github

needs:
Это означает, что пока упсешно не выполнится заданная задача, перехода дальше не будет

${{ secrets.SECRET_NAME }}
Settings -> New repository secret -> SSH_PRIVATE_KEY
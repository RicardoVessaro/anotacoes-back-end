
# TODO usar coonfig com variaveis de ambiente
def get_base_url():

    ip =  'localhost'
    host = f'http://{ip}'
    port = '5001'
    base_url = f'{host}:{port}'

    return base_url
    
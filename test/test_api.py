import request 

if __name__ == '__main__':
    url = 'https://www.google.com.ar'
    response = request.get(url)

    print(response)
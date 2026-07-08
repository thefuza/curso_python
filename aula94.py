# try, except, else, finally
try: #Try pode ser usado com except ou finally
    print('Abrir Arquivo')
    8/0
except ZeroDivisionError as e:
    print(e.__class__.__name__)
    print(e)
    print('Dividiu Zero')
except IndexError as error:
    print('IndexErro')
except (NameError, ImportError):
    print('NameError, ImportError')
else:
    print('Não deu erro')
finally:
    print('Fechar Arquivo')

    # Try except
    # Try except finally
    # Try finally
    # Try except else finally
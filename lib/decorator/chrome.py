from selenium.common import exceptions

def deco_new_searchbox(fn):

    def wrapper(driver):
        try:
            return fn(driver)

        except exceptions.TimeoutException:
            try:
                driver.quit()
            except: pass
            raise Exception('Google Mapsの読み込みに失敗しました。')


        except Exception as e:
            raise e # TODO: more error handlings

    return wrapper


def deco_fetch_coord(fn):

    def wrapper(cls, add, driver, searchbox):
        print(f'fetching coordinates for { add } ...')

        x, y = fn(cls, add, driver, searchbox)

        if x is None:
            msg = f'{ add }:\tfailed to fetch coordinates at { driver.current_url }'
            cls._errs.append(msg)

        return x, y

    return wrapper

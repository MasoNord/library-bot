import requests
from bs4 import BeautifulSoup

async def get_books(query):
    search_url = 'https://spblib.ru/catalog'
    payload = {
        '_ru_spb_iac_esbo_portal_catalog_CatalogPortlet_book-QUERY': query
    }
    search_response = requests.post(search_url, data=payload)

    if search_response.status_code == 200:
        result_url = f"https://spblib.ru/catalog/-/books/available/search/{query.replace(' ', '+')}#search-results"
        result_response = requests.get(result_url)

        if result_response.status_code == 200:
            soup = BeautifulSoup(result_response.text, 'html.parser')
            books = []
            for row in soup.select('tbody.table-data tr'):
                title_tag = row.select_one('td.last a')
                age_category = row.select_one('.age-category')
                copy_status = row.select_one('.search-results-copy-status')

                if title_tag:
                    title = title_tag.text.strip()
                    link = title_tag['href']
                    age = age_category.text.strip() if age_category else "Нет информации о возрасте"
                    status = copy_status.text.strip() if copy_status else "Нет информации о статусе"

                    details = []
                    item_details = row.select_one('.item-details')
                    if item_details:
                        detail_tags = item_details.find_all(['b', 'a'])
                        for i in range(len(detail_tags)):
                            if detail_tags[i].name == 'b':
                                next_tag = detail_tags[i + 1] if i + 1 < len(detail_tags) else None
                                if next_tag and next_tag.name == 'a':
                                    if detail_tags[i].text.strip() == "Автор":
                                        author = next_tag.text.strip()
                                        details.append(f"Автор: {author}")
                                    elif detail_tags[i].text.strip() == "Тематика":
                                        subject = next_tag.text.strip()
                                        details.append(f"Тематика: {subject}")
                                    elif detail_tags[i].text.strip() == "Издательство":
                                        publisher = next_tag.text.strip()
                                        details.append(f"Издательство: {publisher}")
                                    elif detail_tags[i].text.strip() == "Год издания":
                                        year = next_tag.text.strip()
                                        details.append(f"Год издания: {year}")

                    details_str = "\n".join(details) if details else "Нет дополнительных деталей."
                    availability_info = await get_availability(link)
                    books.append(f"\"{title}\" (Возраст: {age})\nСтатус: {status}\n {details_str}\n {availability_info}\n")

            if books:
                return "\n".join(books)
            else:
                return "Книги не найдены."
        else:
            return "Не удалось получить данные с сайта результатов."
    else:
        return "Не удалось выполнить поиск."

async def get_availability(book_url):
    book_response = requests.get(book_url)

    if book_response.status_code == 200:
        book_soup = BeautifulSoup(book_response.text, 'html.parser')
        availability_info = []

        districts = book_soup.select('.tabs .district-group')
        for district in districts:
            district_name = district.select_one('a.pseudo-link').text.strip()
            library_info = district.select_one('.library-information')
            if library_info:
                libraries = library_info.find_all('li', class_='library')
                for library in libraries:
                    library_name = library.select_one('span[itemprop="offeredBy"]').text.strip()
                    availability = library.select_one('.label')
                    availability_text = availability.text.strip() if availability else "Нет информации о наличии"
                    availability_info.append(f"{district_name}: {library_name} - {availability_text}")

        return "\n".join(availability_info) if availability_info else "Нет информации о наличии."
    else:
        return "Не удалось получить информацию о наличии книг"



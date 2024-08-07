import requests
from urllib.parse import urlparse
import os


def download_file_with_url_filename(url, destination_folder='.'):
    """
    주어진 URL에서 파일을 다운로드하여 URL에 명시된 파일명을 사용해 로컬에 저장합니다.

    Parameters:
    url (str): 다운로드할 파일의 URL
    destination_folder (str): 파일을 저장할 로컬 폴더 (기본값은 현재 폴더)

    Returns:
    None
    """
    try:
        # URL을 파싱하여 파일명을 추출합니다.
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # 파일을 저장할 전체 경로를 생성합니다.
        destination_path = os.path.join(destination_folder, filename)

        # URL에 대한 HTTP GET 요청을 보냅니다.
        response = requests.get(url, stream=True)

        # 요청이 성공했는지 확인합니다.
        if response.status_code == 200:
            # 다운로드한 내용을 destination 경로에 작성합니다.
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"파일이 성공적으로 다운로드되었습니다: {destination_path}")
        else:
            print(f"파일을 다운로드할 수 없습니다. 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

import os.path

import scraper
import converter
import sys



if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('not enough arguement to call')
        sys.exit(1)
    input_file = sys.argv[1]
    output_dir=os.path.join(os.path.dirname(input_file),'tmpimgdir/')
    input = open(input_file, 'r')
    for line in input:
        print('start for line:', line)
        try:
            split = line.strip().split(',')
            thsis_name = split[0]
            thsis_img_dir = os.path.join(output_dir, thsis_name)
            thsis_pdf_file = os.path.join(os.path.dirname(input_file), f"{thsis_name}.pdf")
            thsis_id1 = split[1]
            thsis_id2 = split[2]
            thsis_url = f"https://thesis.lib.pku.edu.cn/docinfo.action?id1={thsis_id1}&id2={thsis_id2}"
        except Exception as e:
            print("[main]parse line err:", e)
            continue

        retry=1
        try:
            while True:
                if retry>=4:
                    raise Exception("跳出两层循环")
                try:
                    scraper.scrap_by_url(thsis_name, thsis_url, thsis_img_dir)
                    break
                except Exception as e:
                    print(f"[main]scrape content err:{str(e)},retry times:{retry}")
                    retry += 1
                    continue
        except Exception as e:
            continue


        try:
            converter.convert_images_to_pdf(thsis_img_dir, thsis_pdf_file)
        except Exception as e:
            print("[main]2pdf err:", e)
            continue
    input.close()


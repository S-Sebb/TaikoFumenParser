# -*- coding: utf-8 -*-
from utils import *
import math

course_filename_suffixes = {"_x.bin": "Edit", "_m.bin": "Oni", "_h.bin": "Hard", "_n.bin": "Normal", "_e.bin": "Easy"}


def parse_fumen(fumen_info_dict):
    music_id = fumen_info_dict["music_id"]
    fumen_filepaths = fumen_info_dict["fumen_filepaths"]
    fumen_filenames = fumen_info_dict["fumen_filenames"]
    courses = fumen_info_dict["courses"]

    filled_fumen_info_dict = {
        "id": music_id,
        "shinutiEasy": 0,
        "shinutiNormal": 0,
        "shinutiHard": 0,
        "shinutiMania": 0,
        "shinutiUra": 0,
        "shinutiEasyDuet": 0,
        "shinutiNormalDuet": 0,
        "shinutiHardDuet": 0,
        "shinutiManiaDuet": 0,
        "shinutiUraDuet": 0,
        "shinutiScoreEasy": 0,
        "shinutiScoreNormal": 0,
        "shinutiScoreHard": 0,
        "shinutiScoreMania": 0,
        "shinutiScoreUra": 0,
        "shinutiScoreEasyDuet": 0,
        "shinutiScoreNormalDuet": 0,
        "shinutiScoreHardDuet": 0,
        "shinutiScoreManiaDuet": 0,
        "shinutiScoreUraDuet": 0,
        "easyOnpuNum": 0,
        "normalOnpuNum": 0,
        "hardOnpuNum": 0,
        "maniaOnpuNum": 0,
        "uraOnpuNum": 0,
        "fuusenTotalNormal": 0,
        "fuusenTotalHard": 0,
        "fuusenTotalMania": 0,
        "fuusenTotalUra": 0
    }

    for fumen_filename, fumen_filepath, course in zip(fumen_filenames, fumen_filepaths, courses):
        hex_data = open_as_hex(fumen_filepath)

        start_pos = 568 * 2  # 568 = 0x238 start of fumen data
        note_data_length = 24 * 2
        note_type_length = 4 * 2

        total_balloon_hit_count = 0
        note_type_count = {}
        total_renda_duration = 0
        for j in range(1, 14):
            note_type_count[j] = 0
        try:
            while start_pos < len(hex_data):
                while hex_data[start_pos: start_pos + 4 * 2] == "00000000":
                    start_pos += 64 * 2
                    if start_pos >= len(hex_data):
                        break
                if start_pos >= len(hex_data):
                    break
                note_type_start = start_pos
                note_type_end = note_type_start + note_type_length
                note_type = hex2int(hex_data[note_type_start:note_type_end])
                is_renda = False
                if note_type == 10 or note_type == 12:
                    balloon_hit_count = hex2int(hex_data[start_pos + 16 * 2: start_pos + 20 * 2])
                    if balloon_hit_count < 300:
                        total_balloon_hit_count += balloon_hit_count
                    elif balloon_hit_count < 1000:
                        is_renda = True
                elif note_type == 6 or note_type == 9:
                    is_renda = True
                if is_renda:
                    renda_duration = hex2float(hex_data[start_pos + 20 * 2:start_pos + 24 * 2])
                    total_renda_duration += renda_duration
                note_type_count[note_type] += 1
                if note_type == 6 or note_type == 9:
                    start_pos += 8 * 2
                start_pos += note_data_length

            total_renda_duration /= 1000
            note_sum = 0
            for j in [1, 2, 3, 4, 5, 7, 8]:
                note_sum += note_type_count[j]
            if course == "Edit" or course == "Oni":
                renda_per_sec = 17
            elif course == "Hard":
                renda_per_sec = 11
            elif course == "Normal":
                renda_per_sec = 8
            else:
                renda_per_sec = 6
            score_init = math.ceil(((1000000 - total_balloon_hit_count * 100 -
                                     total_renda_duration * renda_per_sec * 100) / note_sum) / 10) * 10
            score_kiwami = round((total_renda_duration * renda_per_sec * 100 +
                                  note_sum * score_init + total_balloon_hit_count * 100) / 10) * 10
            if course == "Edit":
                filled_fumen_info_dict["shinutiUra"] = score_init
                filled_fumen_info_dict["shinutiUraDuet"] = score_init
                filled_fumen_info_dict["shinutiScoreUra"] = score_kiwami
                filled_fumen_info_dict["shinutiScoreUraDuet"] = score_kiwami
                filled_fumen_info_dict["uraOnpuNum"] = note_sum
                filled_fumen_info_dict["fuusenTotalUra"] = total_balloon_hit_count
            elif course == "Oni":
                filled_fumen_info_dict["shinutiMania"] = score_init
                filled_fumen_info_dict["shinutiManiaDuet"] = score_init
                filled_fumen_info_dict["shinutiScoreMania"] = score_kiwami
                filled_fumen_info_dict["shinutiScoreManiaDuet"] = score_kiwami
                filled_fumen_info_dict["maniaOnpuNum"] = note_sum
                filled_fumen_info_dict["fuusenTotalMania"] = total_balloon_hit_count
            elif course == "Hard":
                filled_fumen_info_dict["shinutiHard"] = score_init
                filled_fumen_info_dict["shinutiHardDuet"] = score_init
                filled_fumen_info_dict["shinutiScoreHard"] = score_kiwami
                filled_fumen_info_dict["shinutiScoreHardDuet"] = score_kiwami
                filled_fumen_info_dict["fuusenTotalHard"] = total_balloon_hit_count
                filled_fumen_info_dict["hardOnpuNum"] = note_sum
            elif course == "Normal":
                filled_fumen_info_dict["shinutiNormal"] = score_init
                filled_fumen_info_dict["shinutiNormalDuet"] = score_init
                filled_fumen_info_dict["shinutiScoreNormal"] = score_kiwami
                filled_fumen_info_dict["shinutiScoreNormalDuet"] = score_kiwami
                filled_fumen_info_dict["fuusenTotalNormal"] = total_balloon_hit_count
                filled_fumen_info_dict["normalOnpuNum"] = note_sum
            elif course == "Easy":
                filled_fumen_info_dict["shinutiEasy"] = score_init
                filled_fumen_info_dict["shinutiEasyDuet"] = score_init
                filled_fumen_info_dict["shinutiScoreEasy"] = score_kiwami
                filled_fumen_info_dict["shinutiScoreEasyDuet"] = score_kiwami
                filled_fumen_info_dict["easyOnpuNum"] = note_sum
        except Exception as e:
            print("\n")
            print("Branching or misaligned data detected in fumen file: %s" % fumen_filepath)
            continue
    return filled_fumen_info_dict


if __name__ == "__main__":
    init()
    filepaths, filenames = enumerate_files(input_path)
    fumen_filepaths = []
    fumen_filenames = []
    fumen_course = []
    fumen_info_dict_list = []
    for filepath, filename in zip(filepaths, filenames):
        for course_filename_suffix in course_filename_suffixes:
            if filename.endswith(course_filename_suffix):
                music_id = filename.split(course_filename_suffix)[0]
                found = False
                idx = -1
                for i, fumen_info_dict in enumerate(fumen_info_dict_list):
                    if fumen_info_dict["music_id"] == music_id:
                        found = True
                        idx = i
                        break
                if not found:
                    fumen_info_dict = {"music_id": music_id, "fumen_filepaths": [], "fumen_filenames": [],
                                       "courses": []}
                fumen_info_dict["fumen_filepaths"].append(filepath)
                fumen_info_dict["fumen_filenames"].append(filename)
                fumen_info_dict["courses"].append(course_filename_suffixes[course_filename_suffix])
                if not found:
                    fumen_info_dict_list.append(fumen_info_dict)
                else:
                    fumen_info_dict_list[idx] = fumen_info_dict
    print("Found %d fumen files" % len(fumen_info_dict_list))
    for fumen_info_dict in fumen_info_dict_list:
        print(fumen_info_dict["music_id"])
    print("\n")

    filled_fumen_info_dict_list = []

    for fumen_info_dict in fumen_info_dict_list:
        filled_fumen_info_dict = parse_fumen(fumen_info_dict)
        filled_fumen_info_dict_list.append(filled_fumen_info_dict)
    write_json(filled_fumen_info_dict_list)
    print("Complete!\n"
          "Output file path: %s\n" % output_json_path)

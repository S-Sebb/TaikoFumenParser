# -*- coding: utf-8 -*-
from utils import *
import math

course_filename_suffixes = {"_x.bin": "Edit", "_m.bin": "Oni", "_h.bin": "Hard", "_n.bin": "Normal", "_e.bin": "Easy"}

def parse_fumen(fumen_filepath, fumen_filename, course):
    fumen_data = {}

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
            if note_type == 10 or 12:
                balloon_hit_count = hex2int(hex_data[start_pos + 20 * 2: start_pos + 24 * 2])
                if balloon_hit_count < 300:
                    total_balloon_hit_count += balloon_hit_count
                else:
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
    except Exception as e:
        print("\n")
        print("Branching or misaligned data detected in fumen file: %s" % fumen_filepath)
        return fumen_data
    fumen_data["fumen_name"] = fumen_filename
    fumen_data["course"] = course
    fumen_data["total_balloon_hit_count"] = total_balloon_hit_count
    fumen_data["total_renda_duration"] = total_renda_duration
    fumen_data["note_type_count"] = note_type_count
    fumen_data["note_sum"] = note_sum
    fumen_data["score_init"] = score_init
    fumen_data["score_kiwami"] = score_kiwami

    return fumen_data

if __name__ == "__main__":
    init()
    filepaths, filenames = enumerate_files(input_path)
    fumen_filepaths = []
    fumen_filenames = []
    fumen_course = []
    for filepath, filename in zip(filepaths, filenames):
        for course_filename_suffix in course_filename_suffixes:
            if filename.endswith(course_filename_suffix):
                fumen_filepaths.append(filepath)
                fumen_filenames.append(filename)
                fumen_course.append(course_filename_suffixes[course_filename_suffix])
                break
    print("Found %d fumen files" % len(fumen_filepaths))
    for filename in fumen_filenames:
        print(filename)
    print("\n")

    fumen_data_list = []

    for filepath, filename, course in zip(fumen_filepaths, fumen_filenames, fumen_course):
        fumen_data = parse_fumen(filepath, filename, course)
        fumen_data_list.append(fumen_data)

    write_json(fumen_data_list)
    print("Complete!\n"
          "Output file path: %s\n" % output_json_path)


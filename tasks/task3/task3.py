def appearance(intervals: dict[str, list[int]]) -> int:
    start_lesson, end_lesson = intervals["lesson"]
    pupil_intervals = intervals["pupil"]
    tutor_intervals = intervals["tutor"]

    def process_intervals(intervals, start_lesson, end_lesson):
        seconds = set()
        for i in range(0, len(intervals), 2):
            start = intervals[i]
            end = intervals[i+1]
            start = max(start, start_lesson)
            end = min(end, end_lesson)
            if start < end:
                seconds.update(range(start, end))
        return seconds

    pupil_set = process_intervals(pupil_intervals, start_lesson, end_lesson)
    tutor_set = process_intervals(tutor_intervals, start_lesson, end_lesson)
    result_set = pupil_set.intersection(tutor_set) 

    return len(result_set)

import inspect
import logging

import decode_qr
import qr_utils
from examgenerator.constants import LIST_ANS_CONVERSION


try:
    from examtemplates import template_generator
except ImportError:
    pass

logging.basicConfig()
global_log = logging.getLogger(__package__)
log = global_log.getChild(__name__.replace(f"{__package__}.", ""))
log.setLevel(global_log.getEffectiveLevel())


def grade(resp, squad="H", explain=False, qr_data=None) -> (int, int):
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    if qr_data is None:
        # I can't work with these conditions!
        return None

    if len(qr_data) > 1:
        print("Error: Encountered more data in QR code than expected.")
        print(f"{qr_data}")
        return None

    template_name = qr_data[0].decode("utf-8")
    mylog.debug(f"QR Data: {template_name}")
    answer_list = list()
    if qr_data[0].startswith(b"RANDOM;"):
        b_list = qr_data[0].replace(b"RANDOM;", "").split()
        answer_list = qr_utils.unpack_bytearray(b_list)
    else:
        try:
            # TODO: Use contents of qr_data[0] to reference generator from VE_exam_generator.
            mylog.debug(f"Collecting from {template_name}")
            gen_output = template_generator(template_name)
            for _ in range(0, 50):
                answer_list.append(LIST_ANS_CONVERSION[next(gen_output)])
            mylog.debug(f"Collected: {answer_list}")
        except ReferenceError:
            print("Template generator not available.")
            exit(1)

    correct = 0
    incorrect = 0
    possibly_incorrect = 0
    q_number = 1
    for q in answer_list:
        q_no = 'q' + str(q_number)
        marked = resp.get(q_no, "X")
        if q == marked:
            correct = correct + 1
        if q != marked and q_number <= 35:
            incorrect = incorrect + 1
        # Handle case of Technician and General exam
        if q != marked and q_number > 35:
            possibly_incorrect = possibly_incorrect + 1
        q_number = q_number + 1

    # Likely a technician or general exam...
    if possibly_incorrect == 15 and correct + incorrect == 35:
        mylog.debug(f"Correct answers: {correct}; incorrect answers: {incorrect}; possibly incorrect: {possibly_incorrect}")
        return correct, incorrect
    else:
        mylog.debug(f"Correct answers: {correct}; incorrect + possibly incorrect answers: {(incorrect + possibly_incorrect)}")
        return correct, (incorrect + possibly_incorrect)


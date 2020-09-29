from django.shortcuts import render
from django.utils.encoding import smart_str

import re
from datetime import datetime

from .models import Smart, Index


def index(request):
    # data upload
    num_uploaded_indexes = -1
    num_uploaded_smarts = -1
    duplicate_indexes = []
    duplicate_smarts = []
    active_indexes = 'show active'
    active_smarts = ''

    if request.POST:
        if request.FILES:
            # append data from a file
            file_type = None
            if 'inputIndexFile' in request.FILES:
                file_type = 'inputIndexFile'
            elif 'inputSmartFile' in request.FILES:
                file_type = 'inputSmartFile'
                active_indexes = ''
                active_smarts = 'show active'

            if file_type:
                csvfile = request.FILES[file_type]
                for row in re.split(r'\n', smart_str(csvfile.read())):
                    fields = re.split(r'\t', row)
                    nmb = fields[0]
                    if len(fields) == 5 and re.match(r'\d+', nmb):
                        sq = fields[1]
                        src = fields[2] if len(fields[2]) > 0 else 'Unknown'
                        dt = fields[3] if len(fields[3]) > 0 else datetime.today().strftime('%Y-%m-%d') # add date/time convertation for input data
                        cmt = fields[4] if len(fields[4]) > 0 else 'No comments'
                        if file_type == 'inputIndexFile':
                            index = Index(number=nmb, seq=sq, source=src, date=dt, comment=cmt)
                            if Index.objects.filter(number=nmb).exists() or Index.objects.filter(seq=sq).exists():
                                duplicate_indexes.append(index)
                            else:
                                index.save()
                                if num_uploaded_indexes == -1:
                                    num_uploaded_indexes = 0
                                num_uploaded_indexes += 1
                        elif file_type == 'inputSmartFile':
                            smart = Smart(number=nmb, seq=sq, source=src, date=dt, comment=cmt)
                            if Smart.objects.filter(number=nmb).exists() or Smart.objects.filter(seq=sq).exists():
                                duplicate_smarts.append(smart)
                            else:
                                smart.save()
                                if num_uploaded_smarts == -1:
                                    num_uploaded_smarts = 0
                                num_uploaded_smarts += 1
        else:
            # delete data from models
            pattern_index = re.compile(r'indexCheck(\d+)')
            pattern_smart = re.compile(r'smartCheck(\d+)')
            show_tab_smart = 0
            for item in request.POST:
                print(item)
                p_index = re.match(pattern_index, item)
                p_smart = re.match(pattern_smart, item)
                if p_index:
                    index_id = p_index.group(1)
                    Index.objects.filter(id=index_id).delete()
                elif p_smart:
                    smart_id = p_smart.group(1)
                    Smart.objects.filter(id=smart_id).delete()
                    show_tab_smart = 1

            if show_tab_smart:
                active_indexes = ''
                active_smarts = 'show active'

    # data request
    index_list = Index.objects.order_by('id')
    smart_list = Smart.objects.order_by('id')
    context = {
        'index_list': index_list,
        'index_total': len(index_list),
        'smart_list': smart_list,
        'smart_total': len(smart_list),
        'num_uploaded_indexes': num_uploaded_indexes,
        'num_uploaded_smarts': num_uploaded_smarts,
        'duplicate_indexes': duplicate_indexes,
        'duplicate_smarts': duplicate_smarts,
        'active_indexes': active_indexes,
        'active_smarts': active_smarts,
    }
    return render(request, 'primers.html', context)

# end of main()

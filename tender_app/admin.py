from django.contrib import admin
from .models import *


admin.site.register(
    [
        Bundle,
        City,
        Company,
        CustomUser,
        Feedback,
        Reply,
        Section,
        Subsection,
        Tender,
        TenderDoc,
        Worker,
        WorkerDoc
    ]
)

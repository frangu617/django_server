from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import DataItem
from datetime import datetime
import pytz
import json

def convert_to_timezone(utc_dt, tz_name):
    try:
        target_tz = pytz.timezone(tz_name)
        return utc_dt.astimezone(target_tz)
    except pytz.UnknownTimeZoneError:
        return utc_dt

@method_decorator(csrf_exempt, name='dispatch')
class DataView(View):

    def get(self, request):
        timezone = request.GET.get('timezone', 'UTC')
        items = DataItem.objects.all().order_by('-timestamp')
        data = [
            {
                "id": item.id,
                "content": item.content,
                "timestamp": convert_to_timezone(item.timestamp, timezone).strftime("You posted this data on %Y-%m-%d at %H:%M:%S")
            } for item in items
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        received_data = json.loads(request.body).get('content', '')
        new_item = DataItem.objects.create(content=received_data)
        timezone = request.GET.get('timezone', 'UTC')
        converted_timestamp = convert_to_timezone(new_item.timestamp, timezone)
        return JsonResponse({
            "message": "Data received!",
            "data": {
                "id": new_item.id,
                "content": new_item.content,
                "timestamp": converted_timestamp.strftime("You posted this data on %Y-%m-%d at %H:%M:%S")
            }
        })

    def put(self, request, data_id):
        item = DataItem.objects.get(id=data_id)
        if not item:
            return JsonResponse({"message": "Data not found"}, status=404)

        new_content = json.loads(request.body).get('content', item.content)
        item.content = new_content
        item.timestamp = datetime.now()
        item.save()

        timezone = request.GET.get('timezone', 'UTC')
        converted_timestamp = convert_to_timezone(item.timestamp, timezone)
        return JsonResponse({"message": "Data updated!", "data": {
            "id": item.id,
            "content": item.content,
            "timestamp": converted_timestamp.strftime("You updated this data on %Y-%m-%d at %H:%M:%S")
        }})

    def delete(self, request, data_id):
        try:
            item = DataItem.objects.get(id=data_id)
            item.delete()
            return JsonResponse({"message": f"Data with ID {data_id} has been deleted!"})
        except DataItem.DoesNotExist:
            return JsonResponse({"message": f"Data with ID {data_id} not found!"}, status=404)

from django.core.paginator import Paginator
from django.http import response
from playerRank_list.models import player_rank
from utils.status_response import StatusResponse
from django.views import View



class Fraction(View):
    def get(self, request):
        request_params = request.GET
        client_name = request_params.get("client_name")
        if not client_name:
            return response.JsonResponse(StatusResponse.error(400, "need client_name"))
        current_page = int(request_params.get("p", 1))
        count = request_params.get("count", 10)
        player_rank_obj = player_rank.objects.all().order_by("-fraction")
        paginator = Paginator(player_rank_obj, count)  # 每页5条记录
        num_pages = paginator.num_pages
        print(num_pages)
        if current_page > num_pages:
            current_page = 1
        page = paginator.page(current_page)  # 获取第一页数据，从1开始
        total = paginator.count
        start_index = (current_page - 1) * 10 + 1
        current_obj = None
        s_index = 1
        player_rank_array = []
        for index, obj in enumerate(page):
            if client_name == obj.client_name:
                current_obj = obj
            player_rank_array.append(
                {"index": start_index + index, "id": obj.id, "client_name": obj.client_name, "fraction": obj.fraction})
        if not current_obj:
            current_obj = player_rank.objects.filter(client_name=client_name).first()
        if current_obj:
            player_rank_array.append({
                "index": s_index,
                "id": current_obj.id,
                "client_name": current_obj.client_name,
                "fraction": current_obj.fraction,
            })

        data = {
            "page": current_page,
            "count": count,
            "total": total,
            "data": player_rank_array
        }
        record = StatusResponse.success(data)
        return response.JsonResponse(data=record)

    def post(self, request):
        request_data = request.POST
        client_name = request_data.get("client_name")
        fraction = request_data.get("fraction")
        if not all([client_name, fraction]):
            return response.JsonResponse(StatusResponse.error(400, "need params client_name, fraction"))
        print(client_name, fraction)
        current_client = player_rank.objects.filter(client_name=client_name).first()
        # 如果存在更新，不存在新增
        if current_client:
            player_rank.objects.filter(client_name=client_name).update(fraction=fraction)
        else:
            player_rank_obj = player_rank(client_name=client_name, fraction=fraction)
            player_rank_obj.save()
        record = StatusResponse.success({})
        return response.JsonResponse(data=record)

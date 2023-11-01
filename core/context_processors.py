from core.models import Notification,History,Transaction


def default(request):
    try:
        notifications = Notification.objects.filter(user=request.user).order_by("-id")[:10]
        history = History.objects.filter(user=request.user).order_by("-id")[:10]

    except:
        notifications = None
        history = None


    try:
        user_profile_pic = request.user.kyc.image
    except Exception as e:
        user_profile_pic = None

        



    return {
        "notifications":notifications,
        "history":history,
        'user_profile_pic':user_profile_pic

    }
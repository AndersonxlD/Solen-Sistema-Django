def custom_constants(request):

    return {
        'MY_CONSTANT': request.user,
    }
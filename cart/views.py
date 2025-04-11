from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_product = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.get_total()
    return render(request, "cart_summary.html",
                  {'cart_products': cart_product, 'quantities': quantities, 'total': total})


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if product_id and product_qty:
            product = get_object_or_404(Product, id=int(product_id))
            cart.add(product=product, quantity=int(product_qty))
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity})
            return response
        messages.success(request, "به سبد خرید اضافه شد")
    return redirect('cart_summary')


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        if product_id is not None:
            cart.delete(product=product_id)
            response = JsonResponse({'product': product_id})
            return response
        messages.success(request, "محصول از سبد خرید حذف شد")
    return JsonResponse({'error': 'Invalid request'}, status=400)


# def cart_delete(request):
#     cart = Cart(request)
#     if request.method == 'POST' and request.POST.get('action') == 'post':
#         try:
#             product_id = int(request.POST.get('product_id'))
#         except (ValueError, TypeError):
#             return JsonResponse({'error': 'شناسه محصول نامعتبر است.'}, status=400)
#
#         try:
#             cart.delete(product=product_id)
#             return JsonResponse({'product': product_id}, status=200)
#         except ProductNotFoundError:  # در صورتی که چنین خطایی تعریف شده باشد.
#             return JsonResponse({'error': 'محصول یافت نشد.'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': f'خطای ناشناخته: {str(e)}'}, status=500)
#
#     return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        if product_id and product_qty:
            cart.update(product=product_id, quantity=product_qty)
            response = JsonResponse({'qty': int(product_qty)})
            return response
        messages.success(request, "سبد خرید ویرایش شد")
    return redirect('cart_summary')

# def cart_update(request):
#     cart = Cart(request)
#     if request.method == 'POST' and request.POST.get('action') == 'post':
#         try:
#             product_id = int(request.POST.get('product_id'))
#             product_qty = int(request.POST.get('product_qty'))
#
#             if product_qty <= 0:
#                 return JsonResponse({'error': 'تعداد محصول باید بیشتر از صفر باشد.'}, status=400)
#
#             cart.update(product=product_id, quantity=product_qty)
#             return JsonResponse({'qty': product_qty}, status=200)
#         except ValueError:
#             return JsonResponse({'error': 'مقادیر نامعتبر هستند.'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#
#     return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)

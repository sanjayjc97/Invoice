from .models import (
    Invoice,
    Invoice_details
)

from .serializers import (
    Invoice_serializer,
    List_invoice_serializer
)

from core.utils import (
    is_user_owner
)

from rest_framework import (
    response,
    views,
    status,
    permissions
)

# from rest_framework.permissions import AllowAny,IsAuthenticated

class List_invoice(views.APIView):
    permission_classes=(permissions.IsAuthenticated,)
    def get(self,request):

        try:
            invoice_instance = Invoice.objects.filter(customer_name_id = request.user)
            if invoice_instance:
                serializer = List_invoice_serializer(instance=invoice_instance,many=True)
                return response.Response({"status":1,'message':"Success","data":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return response.Response({"status":0,'message':"No invoices found for this user","data":None},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response. Response({
                'status':0,
                "message":str(e),
                'data':None
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class Create_invoice(views.APIView):
    ''' create a new invoice '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        
        try:
            serializer = Invoice_serializer(data = request.data)
            if serializer.is_valid():
                serializer.save(customer_name = request.user)
                return response.Response({
                    'status':1,
                    "message":"Invoice created successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
            
            else:
                return response.Response({
                    'status':0,
                    'message':serializer.errors,
                    "data":None
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return response.Response({
                'status':0,
                'message':str(e),
                'data':None
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Update_invoice(views.APIView):
    def put(self, request,*args,**kwargs):
        try:
            invoice = Invoice.objects.get(slug_field=request.data.get('slug_field'))
        except Exception as e :
            return response.Response({
                'status': 0,
                'message': "Invocice does not exist",
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        is_verified = is_user_owner(invoice.customer_name,request.user)
        if is_verified:
            serializer = Invoice_serializer(invoice, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(customer_name = request.user)
                return response.Response({
                    'status': 1,
                    'message': "Invoice updated successfully",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return response.Response({
                    'status': 0,
                    'message': serializer.errors,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
        




class Delete_invoice(views.APIView):
    ''' delete a invoice with given slug '''
    def delete(self,request,*args,**kwargs):
        try:
            invoice_slug  = request.data.get('slug_field')
            if invoice_slug:
                invoice = Invoice.objects.get(slug_field=invoice_slug)
                
                if invoice:
                    is_verified = is_user_owner(invoice.customer_name,request.user)
                    if is_verified:
                        invoice.delete()
                        return response.Response({
                            'status':1,
                            'message':"invoice deleted successfully",
                            'data':None
                        },status=status.HTTP_200_OK)
                    else:
                        return response.Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
                else:
                    return response.Response({
                        'status':0,
                        'message':"invoice does not exist",
                        "data":None

                    },status=status.HTTP_404_NOT_FOUND)
            else:
                return response.Response({
                    'status':0,
                    'message':"Please provide invoice slug to be deleted",
                    'data':None
                },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({
                    'status':0,
                    'message':"Internal server error",
                    'data':None
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Invoice_details(views.APIView):
    def post(self,request,*args,**kwargs):
        try:
            invoice = Invoice.objects.get(slug_field=request.data.get('slug_field'))
        except Exception as e :
            return response.Response({
                'status': 0,
                'message': "invoice does not exist",
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        is_verified = is_user_owner(invoice.customer_name,request.user)
        if is_verified:
            serializer = Invoice_serializer(invoice)
            return response.Response({
                    'status': 1,
                    'message': "success",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        else:
            return response.Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
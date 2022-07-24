import logging
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CertSerializer
from .models import Cert
import subprocess
import re

# import os

# Create your views here.
class CertView(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def create(self, request):

        # get latest nonce
        query_results = Cert.objects.latest("nonce")
        latest_nonce = query_results.nonce
        print("latest nonce=%s", latest_nonce)

        # issue cert
        # ROOT_DIR = os.path.abspath(os.curdir)
        # print("ROOT_DIR=%s", ROOT_DIR)
        var = subprocess.Popen(
            ["sh", "../test.sh", str(latest_nonce)],
            stdout=subprocess.PIPE,
        )
        output = var.communicate()
        print("output = ", output)
        logging.INFO("output=%s", str(output))

        # get txn id from docker output
        txnIdList = re.findall(r"txid (.*)\\n\[issue\-cert\]", str(output))
        # logging.INFO("txnIdList=%s", txnIdList)
        print("txnIdList from log: ", txnIdList)
        if len(txnIdList) == 0 or txnIdList[0]:
            return Response(
                {
                    "error": "txnId is null, txn failed to broadcast to ethereum",
                    "output": str(output),
                },
                status=400,
            )

        # POST and update serializer
        newData = request.POST.copy()
        newData["nonce"] = latest_nonce + 1
        newData["txnId"] = txnIdList[0]

        print("newData =", newData)
        serializer = self.get_serializer(data=newData)
        serializer.is_valid(raise_exception=True)
        super().perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

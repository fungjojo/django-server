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

        # reset data
        newData = request.POST.copy()
        if newData["certDataString"] == "reset":
            serializer = self.get_serializer(data=newData)
            serializer.is_valid(raise_exception=True)
            super().perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)

        # write certDataString to json file
        open("../../cert-issuer/data/unsigned_certificates/test1.json", "w").write(
            newData["certDataString"]
        )
        # print("open and read", open("test.json").read())

        # get latest nonce
        query_results = Cert.objects.order_by("-nonce")[0]
        latest_nonce = query_results.nonce
        new_nonce = latest_nonce + 1
        print("latest nonce=", latest_nonce)

        # issue cert
        # ROOT_DIR = os.path.abspath(os.curdir)
        # print("ROOT_DIR=%s", ROOT_DIR)
        var = subprocess.Popen(
            ["sh", "../test.sh", str(new_nonce)],
            stdout=subprocess.PIPE,
        )
        output = var.communicate()
        print("output = ", output)
        # logging.INFO("output=%s", str(output))
        # get txn id from docker output
        dockerLogFile = open("/tmp/docker_log.log", "r").read()
        signedCertFile = open("/tmp/blockchain_certificates/test1.json", "r").read()
        txnIdList = re.findall(r"txid (.*)", str(dockerLogFile))
        print("txnIdList from log: ", txnIdList)
        if len(txnIdList) == 0:
            return Response(
                {
                    "error": "txnId is null, txn failed to broadcast to ethereum",
                    "dockerLogFile": str(dockerLogFile),
                    "txnIdList": str(txnIdList),
                },
                status=400,
            )

        # POST and update serializer
        newData["nonce"] = new_nonce
        newData["txnId"] = txnIdList[0]
        newData["certDataString"] = str(signedCertFile)

        print("newData =", newData)
        serializer = self.get_serializer(data=newData)
        serializer.is_valid(raise_exception=True)
        super().perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

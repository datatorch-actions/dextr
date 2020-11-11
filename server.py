from concurrent import futures
import logging

import grpc

# from dextr import DEXTR

import dextr_pb2_grpc
import dextr_pb2


class Route(dextr_pb2_grpc.RouteServicer):
    def Predict(self, request, context):
        return dextr_pb2.Points(points=[0, 0, 30, 30])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dextr_pb2_grpc.add_RouteServicer_to_server(Route(), server)
    server.add_insecure_port("localhost:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

# def create_mode(weights_path: str):
#     global model
#     model = DEXTR(
#         nb_classes=1,
#         resnet_layers=101,
#         input_shape=(512, 512),
#         weights_path=weights_path,
#         num_input_channels=4,
#         classifier="psp",
#         sigmoid=True,
#     )

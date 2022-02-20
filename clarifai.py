import random
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

# Insert here the initialization code as outlined on this page:
# https://docs.clarifai.com/api-guide/api-overview

# This is how you authenticate.
metadata = (('authorization', f'Key ae39fe44a78d4ebc8a0ef0cac883e9c6'),)

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_json_channel())

userDataObject = resources_pb2.UserAppIDSet(user_id='blmw0pa923pm', app_id='TreeHacks2022')

def get_images(label):
  post_annotations_searches_response = stub.PostAnnotationsSearches(
    service_pb2.PostAnnotationsSearchesRequest(
        searches = [
            resources_pb2.Search(
                query=resources_pb2.Query(
                    filters=[
                        resources_pb2.Filter(
                            annotation=resources_pb2.Annotation(
                                data=resources_pb2.Data(
                                    concepts=[  # You can search by multiple concepts.
                                        resources_pb2.Concept(
                                            id=label,  # You could search by concept Name as well.
                                            value=1  # Value of 0 will search for images that don't have the concept.
                                        )
                                    ]
                                )
                            )
                        )
                    ]
                )
            )
        ]
    ),
    metadata=metadata
  )

  if post_annotations_searches_response.status.code != status_code_pb2.SUCCESS:
      raise Exception("Post searches failed, status: " + post_annotations_searches_response.status.description)

  images = []
  for hit in post_annotations_searches_response.hits :
  #     print("\tScore %.2f for annotation: %s url: %s" % (hit.score, hit.annotation.id, hit.input.id))
      images.append(hit.input.data.image.url)
  return images 
  
def get_all_images():
  # This is how you authenticate.
  metadata = (('authorization', f'Key ae39fe44a78d4ebc8a0ef0cac883e9c6'),)
  stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
  
  post_annotations_searches_response = stub.PostAnnotationsSearches(
      service_pb2.PostAnnotationsSearchesRequest(
          searches = [
              resources_pb2.Search(
                  query=resources_pb2.Query(
                      filters=[
                          resources_pb2.Filter(
                              annotation=resources_pb2.Annotation(
                                  data=resources_pb2.Data()
                              )
                          )
                      ]
                  )
              )
          ]
      ),
      metadata=metadata
  )
  
  if post_annotations_searches_response.status.code != status_code_pb2.SUCCESS:
      raise Exception("Post searches failed, status: " + post_annotations_searches_response.status.description)
  
  hits = []
  for hit in post_annotations_searches_response.hits:
      hits.append(hit.input.data.image.url)
      
  return hits
  
def upload_db_t(bytes, classification):
  print("uploading image with classification ", classification)
  post_inputs_response = stub.PostInputs(
    service_pb2.PostInputsRequest(
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=bytes
                    ),
                    concepts=[resources_pb2.Concept(id=classification, value=1)]
                )
            )
        ]
    ),
    metadata=metadata
  )

  if post_inputs_response.status.code != status_code_pb2.SUCCESS:
      print("There was an error with your request!")
      print("\tCode: {}".format(post_inputs_response.outputs[0].status.code))
      print("\tDescription: {}".format(post_inputs_response.outputs[0].status.description))
      print("\tDetails: {}".format(post_inputs_response.outputs[0].status.details))
      raise Exception("Post inputs failed, status: " + post_inputs_response.status.description)

def classify_image(image_bytes):
  


    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id="grey2",
            # version_id="def4cb8d006b4f50a714f50392221476",  # This is optional. Defaults to the latest model version.
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print("There was an error with your request!")
        print(post_model_outputs_response)
        print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
        print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
        print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]

    # print("Predicted concepts:")
    obj = {}
    topK = 3
    for concept in output.data.concepts:
        obj[concept.name] = concept.value
        topK -= 1
        if topK < 0:
          break
    return obj

def get_concepts():
    # Insert here the initialization code as outlined on this page:
    # https://docs.clarifai.com/api-guide/api-overview/api-clients#client-installation-instructions
    list_concepts_response = stub.ListConcepts(
        service_pb2.ListConceptsRequest(),
        metadata=metadata
    )
    all_concepts = []
    if list_concepts_response.status.code != status_code_pb2.SUCCESS:
        print("There was an error with your request!")
        print("\tCode: {}".format(list_concepts_response.outputs[0].status.code))
        print("\tDescription: {}".format(list_concepts_response.outputs[0].status.description))
        print("\tDetails: {}".format(list_concepts_response.outputs[0].status.details))
        raise Exception("List concept failed, status: " +    list_concepts_response.status.description)
    for concept in list_concepts_response.concepts:
        all_concepts.append(concept.name)
    return all_concepts
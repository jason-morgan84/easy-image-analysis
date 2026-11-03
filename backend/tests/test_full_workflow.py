# create graph with single source, correct input data and connections | all nodes run<br> all nodes needs_update flag set to False <br> all nodes is_ready set to True |
# create graph with two sources, correct connections and input_data from one source | all expected nodes run<br> all run nodes needs_update flag set to False <br> all run nodes is_ready flag set to True |

# need nodes:
#       * select channel
#       * select slice
#       * z project
#       * calculate auto-threshold
#       * apply threshold

from core.image_operation_directory import ImageOperationDirectory
from core.workflow import WorkFlow
import numpy as np

def test_full_workflow():
    log = []
    directory = ImageOperationDirectory(logger = log)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # create the following structure:
    # load_image
    #   |
    #   v
    # select_channel ---------> z_project
    #   |                           |
    #   V                           V
    # select_slice             gaussian_filter
    #   |                           |
    #   V                           V
    # gaussian_filter       calculate_auto_threshold
    #   |                           |
    #   V                           |
    # apply_threshold_value <-------
    #   |
    #   V
    # save_image

    workflow.add_node(directory["load_image"])                  # node0: node.load_image.0
    workflow.add_node(directory["select_channel"])              # node1: node.select_channel.1
    workflow.add_node(directory["z_project"])                   # node2: node.z_project.2
    workflow.add_node(directory["gaussian_filter"])             # node3: node.gaussian_filter.3
    workflow.add_node(directory["calculate_auto_threshold"])    # node4: node.calculate_auto_threshold.4
    workflow.add_node(directory["select_slice"])                # node5: node.select_slice.5
    workflow.add_node(directory["gaussian_filter"])             # node6: node.gaussian_filter.6
    workflow.add_node(directory["apply_threshold_value"])       # node7: node.apply_threshold_value.7
    workflow.add_node(directory["save_image"])                  # node8: node.save_image.8

    workflow.add_connection(source_port = workflow.nodes["node.load_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.select_channel.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.select_channel.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.z_project.2"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.z_project.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.gaussian_filter.3"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.gaussian_filter.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.calculate_auto_threshold.4"].input_ports["image.input"])

    workflow.add_connection(source_port = workflow.nodes["node.select_channel.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.select_slice.5"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.select_slice.5"].output_ports["image.output"],
                            target_port = workflow.nodes["node.gaussian_filter.6"].input_ports["image.input"])

    workflow.add_connection(source_port = workflow.nodes["node.calculate_auto_threshold.4"].output_ports["parameter.threshold"],
                            target_port = workflow.nodes["node.apply_threshold_value.7"].input_ports["parameter.threshold"])
    workflow.add_connection(source_port = workflow.nodes["node.gaussian_filter.6"].output_ports["image.output"],
                            target_port = workflow.nodes["node.apply_threshold_value.7"].input_ports["image.input"])

    workflow.add_connection(source_port = workflow.nodes["node.apply_threshold_value.7"].output_ports["image.output"],
                            target_port = workflow.nodes["node.save_image.8"].input_ports["image.input"])


    workflow.nodes["node.load_image.0"].input_ports["parameter.path"].data = ".\\backend\\tests\\test_images\\test_image_8bit.tif"
    workflow.nodes["node.load_image.0"].input_ports["parameter.shape"].data = "ZCYX"

    workflow.nodes["node.z_project.2"].input_ports["parameter.method"].data = "Max intensity"

    workflow.nodes["node.select_channel.1"].input_ports["parameter.channel"].data = np.uint8(1)

    workflow.nodes["node.select_slice.5"].input_ports["parameter.slice"].data = np.uint8(3)

    workflow.nodes["node.gaussian_filter.3"].input_ports["parameter.sigma"].data = np.uint8(3)
    workflow.nodes["node.gaussian_filter.6"].input_ports["parameter.sigma"].data = np.uint8(3)

    workflow.nodes["node.calculate_auto_threshold.4"].input_ports["parameter.method"].data = "Yen"

    workflow.nodes["node.save_image.8"].input_ports["parameter.path"].data = ".\\backend\\tests\\test_images\\test_full_workflow_output.tif"

    from core.error_handling import log as logging


    for node in workflow.nodes.values():
        node.needs_update = True
    workflow.update_graph(test=True)

    for item in log:
        print(f"\n{item.identifier}: {item.message}")

<?xml version="1.0" encoding="UTF-8"?>
<conceptualSchema version="TJ1.0">
    <databaseConnection>
        <embed url="/E:/_3_Master/Applied-Computational-Intelligence-UBB/Year1_Semester2_KnowledgeDiscovery/FinalProject/PreProcessedDataset_150_ShiftBalanced.sql" />
        <table name="PREPROCESSEDDATASET" />
        <key name="TIMESTAMP" />
    </databaseConnection>
    <diagram title="Nominal_Scale_RUL_Class">
        <node id="0">
            <position x="-17.0" y="60.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Medium') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Low') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Healthy') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Critical')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-147.0" y="170.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Healthy'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Healthy</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="80.5" y="82.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Critical'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Critical</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-50.5" y="362.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="33.0" y="50.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="1" to="2" />
        <edge from="1" to="3" />
        <edge from="0" to="4" />
        <edge from="2" to="4" />
        <edge from="3" to="4" />
        <edge from="5" to="4" />
        <edge from="1" to="5" />
        <projectionBase>
            <vector x="80.5" y="82.5" />
            <vector x="33.0" y="50.0" />
            <vector x="-17.0" y="60.0" />
            <vector x="-147.0" y="170.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Thermall_Stress_Temperature">
        <node id="0">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="4" to="0" />
        <edge from="4" to="1" />
        <edge from="4" to="2" />
        <edge from="0" to="3" />
        <edge from="1" to="3" />
        <edge from="2" to="3" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Thermall_Measured_Temperature1">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT1_CELSIUS_DEG_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="0" to="1" />
        <edge from="0" to="2" />
        <edge from="0" to="3" />
        <edge from="1" to="4" />
        <edge from="2" to="4" />
        <edge from="3" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Thermall_Measured_Temperature2">
        <node id="0">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_MEASUREMENT2_CELSIUS_DEG_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="4" to="0" />
        <edge from="4" to="1" />
        <edge from="0" to="2" />
        <edge from="1" to="2" />
        <edge from="3" to="2" />
        <edge from="4" to="3" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Cooling_Efficiency_Total">
        <node id="0">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TOTAL_COOLING_CONSUMPTION_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="1" to="2" />
        <edge from="1" to="3" />
        <edge from="0" to="4" />
        <edge from="2" to="4" />
        <edge from="3" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Cooling_Efficiency_Average">
        <node id="0">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.AVERAGE_COOLING_CONSUMPTION_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="0" />
        <edge from="2" to="1" />
        <edge from="0" to="3" />
        <edge from="1" to="3" />
        <edge from="4" to="3" />
        <edge from="2" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="Nominal_Scale_Cooling_Efficiency_TempDelta">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.TEMPERATURE_DIFFERENCE_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="1" />
        <edge from="3" to="1" />
        <edge from="4" to="1" />
        <edge from="0" to="2" />
        <edge from="0" to="3" />
        <edge from="0" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Cooling_Efficiency_Water_Consumption">
        <node id="0">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.WATER_CONSUMPTION_LITER_MINUTE_FCA_BIN = 'Constant'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Constant</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.WATER_CONSUMPTION_LITER_MINUTE_FCA_BIN = 'Constant')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Cooling_Efficiency_Water_TempDelta">
        <node id="0">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.WATER_TEMPERATURE_DELTA_CELSIUS_DEG_FCA_BIN = 'Constant'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Constant</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.WATER_TEMPERATURE_DELTA_CELSIUS_DEG_FCA_BIN = 'Constant')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Load_Steel_Weight">
        <node id="0">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_TONN_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="2" to="0" />
        <edge from="3" to="0" />
        <edge from="4" to="1" />
        <edge from="4" to="2" />
        <edge from="4" to="3" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Load_Steel_Weight_Theoretical">
        <node id="0">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.STEEL_WEIGHT_THEORETICAL_TONN_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="3" to="0" />
        <edge from="3" to="1" />
        <edge from="3" to="2" />
        <edge from="0" to="4" />
        <edge from="1" to="4" />
        <edge from="2" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Load_Quantity_Ton">
        <node id="0">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.QUANTITY_TONN_FCA_BIN = 'Constant'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Constant</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.QUANTITY_TONN_FCA_BIN = 'Constant')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Load_Cast_In_Row">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CAST_IN_ROW_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="0" to="1" />
        <edge from="0" to="2" />
        <edge from="1" to="3" />
        <edge from="2" to="3" />
        <edge from="4" to="3" />
        <edge from="0" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Impurity_Index">
        <node id="0">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.IMPURITY_INDEX_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="3" to="0" />
        <edge from="0" to="1" />
        <edge from="2" to="1" />
        <edge from="4" to="1" />
        <edge from="3" to="2" />
        <edge from="3" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Composition_Carbon">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="3">NOT (PREPROCESSEDDATASET.C_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.C_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.C_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="0">PREPROCESSEDDATASET.C_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="0">High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="2">PREPROCESSEDDATASET.C_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="2">Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="1">PREPROCESSEDDATASET.C_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="1">Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="1" />
        <edge from="3" to="1" />
        <edge from="4" to="1" />
        <edge from="0" to="2" />
        <edge from="0" to="3" />
        <edge from="0" to="4" />
        <projectionBase>
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
            <vector x="76.0" y="90.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Composition_Chromium">
        <node id="0">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CR_FCA_BIN = 'High'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>High</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CR_FCA_BIN = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.CR_FCA_BIN = 'Medium') AND NOT (PREPROCESSEDDATASET.CR_FCA_BIN = 'Low') AND NOT (PREPROCESSEDDATASET.CR_FCA_BIN = 'High')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.CR_FCA_BIN = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="3" to="0" />
        <edge from="0" to="1" />
        <edge from="2" to="1" />
        <edge from="4" to="1" />
        <edge from="3" to="2" />
        <edge from="3" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="OrdSca_ExcBound_Stream">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&lt;=1)</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-280.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;5) AND (NUM_STREAM&lt;=6)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-224.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;4) AND (NUM_STREAM&lt;=5)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;4</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-168.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;3) AND (NUM_STREAM&lt;=4)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;3</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;1) AND (NUM_STREAM&lt;=2)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-112.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;2) AND (NUM_STREAM&lt;=3)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-336.0" y="1440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_STREAM&gt;6)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;6</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="1" />
        <edge from="3" to="2" />
        <edge from="5" to="3" />
        <edge from="0" to="4" />
        <edge from="4" to="5" />
        <edge from="1" to="6" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="OrdSca_IncBound_Crystalizer">
        <node id="0">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-280.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&gt;24)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;24</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&lt;=1)</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-224.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;18</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-168.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;12</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-112.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;6</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="0" />
        <edge from="3" to="1" />
        <edge from="4" to="3" />
        <edge from="5" to="4" />
        <edge from="0" to="5" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="NomSca_Shift">
        <node id="0">
            <position x="76.0" y="90.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.SHIFT = 'Night'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Night</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.SHIFT = 'Night') AND NOT (PREPROCESSEDDATASET.SHIFT = 'Morning') AND NOT (PREPROCESSEDDATASET.SHIFT = 'Afternoon')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="6.0" y="80.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.SHIFT = 'Afternoon'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Afternoon</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-134.0" y="180.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.SHIFT = 'Morning'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Morning</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-52.0" y="350.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="1" to="2" />
        <edge from="1" to="3" />
        <edge from="0" to="4" />
        <edge from="2" to="4" />
        <edge from="3" to="4" />
        <projectionBase>
            <vector x="76.0" y="90.0" />
            <vector x="6.0" y="80.0" />
            <vector x="-134.0" y="180.0" />
        </projectionBase>
    </diagram>
    <diagram title="GrdSca_ThermalStress_x_Cooling">
        <node id="0">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="24">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-2.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="26">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-332.0" y="1480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="13">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="14">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="8">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="29">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="8">TEMPERATURE_DIFFERENCE_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="28">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-276.0" y="1160.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="20">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="17">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="5">TEMPERATURE_DIFFERENCE_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="25">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-2.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="7">TOTAL_COOLING_CONSUMPTION_SCALED &gt;-2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="2">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="1">TEMPERATURE_DIFFERENCE_SCALED &gt;-2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="19">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-2.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="11">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-2.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="10">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="3">TOTAL_COOLING_CONSUMPTION_SCALED &gt;-6.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-488.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="15">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="-328.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="16">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="-380.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="22">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="0">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="6">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-540.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="21">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="6">TOTAL_COOLING_CONSUMPTION_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="1">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="0">TEMPERATURE_DIFFERENCE_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="5">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="-436.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="23">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="3">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="2">TOTAL_COOLING_CONSUMPTION_SCALED &gt;-4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="-224.0" y="1280.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="9">((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="18">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="-384.0" y="1360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="7">((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="4">((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-2.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="-432.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="12">((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="4">TOTAL_COOLING_CONSUMPTION_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="27">((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0)) AND ((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="25" to="0" />
        <edge from="27" to="0" />
        <edge from="18" to="1" />
        <edge from="8" to="1" />
        <edge from="24" to="2" />
        <edge from="26" to="2" />
        <edge from="1" to="3" />
        <edge from="5" to="3" />
        <edge from="13" to="4" />
        <edge from="10" to="4" />
        <edge from="8" to="5" />
        <edge from="0" to="7" />
        <edge from="15" to="7" />
        <edge from="20" to="8" />
        <edge from="23" to="9" />
        <edge from="6" to="10" />
        <edge from="0" to="11" />
        <edge from="21" to="11" />
        <edge from="29" to="12" />
        <edge from="9" to="12" />
        <edge from="6" to="13" />
        <edge from="19" to="14" />
        <edge from="16" to="14" />
        <edge from="27" to="15" />
        <edge from="16" to="15" />
        <edge from="12" to="16" />
        <edge from="28" to="16" />
        <edge from="18" to="17" />
        <edge from="29" to="17" />
        <edge from="4" to="18" />
        <edge from="20" to="18" />
        <edge from="28" to="19" />
        <edge from="10" to="20" />
        <edge from="3" to="21" />
        <edge from="25" to="21" />
        <edge from="14" to="22" />
        <edge from="15" to="22" />
        <edge from="13" to="23" />
        <edge from="7" to="24" />
        <edge from="11" to="24" />
        <edge from="1" to="25" />
        <edge from="17" to="25" />
        <edge from="7" to="26" />
        <edge from="22" to="26" />
        <edge from="17" to="27" />
        <edge from="12" to="27" />
        <edge from="9" to="28" />
        <edge from="4" to="29" />
        <edge from="23" to="29" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GrdSca_ProductionLoad_x_ThermalStress">
        <node id="0">
            <position x="-440.0" y="1680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;0.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-652.0" y="1640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-488.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-1.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=0.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-7.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-5.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-276.0" y="1160.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-2.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-4.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-2.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-4.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-2.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-596.0" y="1320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;0.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-7.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-5.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-7.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-5.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-7.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-5.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;-7.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="-648.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;0.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;0.5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&lt;=-7.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-4.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-2.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-540.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-1.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=0.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;-1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="-328.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-2.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="-756.0" y="1400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="-548.0" y="1880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-332.0" y="1480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-1.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=0.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-436.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-1.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=0.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="-544.0" y="1440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;0.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="-224.0" y="1280.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-2.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="-704.0" y="1520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-4.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-2.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-5.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-4.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&lt;=-7.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&lt;=-7.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="-492.0" y="1560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;0.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&lt;=-7.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;-2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="-600.0" y="1760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="30">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-7.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-5.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="31">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-5.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-4.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="32">
            <position x="-384.0" y="1360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-1.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=0.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="33">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-5.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-4.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="34">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-4.0) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-2.5)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;-4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="35">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-5.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-4.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="36">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-5.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-4.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;-5.5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="37">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&lt;=-7.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="38">
            <position x="-380.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-2.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="39">
            <position x="-432.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_WEIGHT_TONN_SCALED&gt;-2.5) AND (STEEL_WEIGHT_TONN_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_WEIGHT_TONN_SCALED &gt;-2.5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <edge from="18" to="0" />
        <edge from="27" to="0" />
        <edge from="20" to="1" />
        <edge from="22" to="1" />
        <edge from="14" to="2" />
        <edge from="38" to="2" />
        <edge from="9" to="3" />
        <edge from="12" to="3" />
        <edge from="13" to="4" />
        <edge from="15" to="4" />
        <edge from="24" to="5" />
        <edge from="6" to="5" />
        <edge from="34" to="6" />
        <edge from="33" to="6" />
        <edge from="2" to="7" />
        <edge from="11" to="7" />
        <edge from="26" to="8" />
        <edge from="3" to="8" />
        <edge from="25" to="9" />
        <edge from="30" to="9" />
        <edge from="37" to="10" />
        <edge from="14" to="11" />
        <edge from="25" to="12" />
        <edge from="5" to="13" />
        <edge from="31" to="13" />
        <edge from="39" to="14" />
        <edge from="5" to="15" />
        <edge from="38" to="15" />
        <edge from="11" to="16" />
        <edge from="0" to="17" />
        <edge from="29" to="17" />
        <edge from="21" to="18" />
        <edge from="32" to="18" />
        <edge from="2" to="19" />
        <edge from="15" to="19" />
        <edge from="7" to="20" />
        <edge from="19" to="20" />
        <edge from="4" to="21" />
        <edge from="23" to="21" />
        <edge from="7" to="22" />
        <edge from="16" to="22" />
        <edge from="35" to="23" />
        <edge from="13" to="23" />
        <edge from="9" to="24" />
        <edge from="33" to="24" />
        <edge from="28" to="25" />
        <edge from="12" to="26" />
        <edge from="20" to="27" />
        <edge from="32" to="27" />
        <edge from="37" to="28" />
        <edge from="1" to="29" />
        <edge from="27" to="29" />
        <edge from="10" to="30" />
        <edge from="28" to="30" />
        <edge from="24" to="31" />
        <edge from="3" to="31" />
        <edge from="4" to="32" />
        <edge from="19" to="32" />
        <edge from="30" to="33" />
        <edge from="36" to="33" />
        <edge from="36" to="34" />
        <edge from="31" to="35" />
        <edge from="8" to="35" />
        <edge from="10" to="36" />
        <edge from="6" to="38" />
        <edge from="39" to="38" />
        <edge from="34" to="39" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GriSca_Impurity_x_ThermalStress">
        <node id="0">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-2.0) AND (IMPURITY_INDEX_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-1.0) AND (IMPURITY_INDEX_SCALED&lt;=0.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-488.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-2.0) AND (IMPURITY_INDEX_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-1.0) AND (IMPURITY_INDEX_SCALED&lt;=0.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-2.0) AND (IMPURITY_INDEX_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;0.0) AND (IMPURITY_INDEX_SCALED&lt;=1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-328.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;1.0) AND (IMPURITY_INDEX_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="-384.0" y="1360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;0.0) AND (IMPURITY_INDEX_SCALED&lt;=1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&lt;=-2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="-224.0" y="1280.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;1.0) AND (IMPURITY_INDEX_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;0.0) AND (IMPURITY_INDEX_SCALED&lt;=1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-540.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>IMPURITY_INDEX_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;0.0) AND (IMPURITY_INDEX_SCALED&lt;=1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="-380.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;1.0) AND (IMPURITY_INDEX_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="-432.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;1.0) AND (IMPURITY_INDEX_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>IMPURITY_INDEX_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&lt;=-2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-1.0) AND (IMPURITY_INDEX_SCALED&lt;=0.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-1.0) AND (IMPURITY_INDEX_SCALED&lt;=0.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>IMPURITY_INDEX_SCALED &gt;-1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&lt;=-2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="-436.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-2.0) AND (IMPURITY_INDEX_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&lt;=-2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&lt;=-2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;-2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TEMPERATURE_DIFFERENCE_SCALED &gt;-2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-2.0) AND (IMPURITY_INDEX_SCALED&lt;=-1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>IMPURITY_INDEX_SCALED &gt;-2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;-1.0) AND (IMPURITY_INDEX_SCALED&lt;=0.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;0.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;0.0) AND (IMPURITY_INDEX_SCALED&lt;=1.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&lt;=-2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>IMPURITY_INDEX_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="-332.0" y="1480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="-276.0" y="1160.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((IMPURITY_INDEX_SCALED&gt;1.0) AND (IMPURITY_INDEX_SCALED&lt;=2.0)) AND ((TEMPERATURE_DIFFERENCE_SCALED&gt;2.0) AND (TEMPERATURE_DIFFERENCE_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <edge from="22" to="0" />
        <edge from="17" to="0" />
        <edge from="3" to="1" />
        <edge from="4" to="1" />
        <edge from="13" to="2" />
        <edge from="15" to="2" />
        <edge from="10" to="3" />
        <edge from="5" to="3" />
        <edge from="5" to="4" />
        <edge from="26" to="4" />
        <edge from="0" to="5" />
        <edge from="23" to="5" />
        <edge from="14" to="6" />
        <edge from="1" to="6" />
        <edge from="15" to="7" />
        <edge from="9" to="7" />
        <edge from="21" to="8" />
        <edge from="29" to="8" />
        <edge from="26" to="9" />
        <edge from="12" to="9" />
        <edge from="23" to="10" />
        <edge from="6" to="11" />
        <edge from="29" to="11" />
        <edge from="18" to="12" />
        <edge from="27" to="12" />
        <edge from="16" to="13" />
        <edge from="4" to="14" />
        <edge from="9" to="14" />
        <edge from="16" to="15" />
        <edge from="12" to="15" />
        <edge from="27" to="16" />
        <edge from="24" to="17" />
        <edge from="22" to="18" />
        <edge from="19" to="18" />
        <edge from="25" to="19" />
        <edge from="2" to="21" />
        <edge from="7" to="21" />
        <edge from="24" to="22" />
        <edge from="25" to="22" />
        <edge from="17" to="23" />
        <edge from="20" to="24" />
        <edge from="20" to="25" />
        <edge from="0" to="26" />
        <edge from="18" to="26" />
        <edge from="19" to="27" />
        <edge from="8" to="28" />
        <edge from="11" to="28" />
        <edge from="14" to="29" />
        <edge from="7" to="29" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GriSca_Cooling_x_RUL">
        <node id="0">
            <position x="-436.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="152.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-384.0" y="1360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-224.0" y="1280.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-12.0" y="1320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-492.0" y="1560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="-332.0" y="1480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="-548.0" y="1880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="96.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="-704.0" y="1520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-600.0" y="1760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;-4.5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;-6.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="-652.0" y="1640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="-388.0" y="1800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;-1.5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="-432.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;3.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="-756.0" y="1400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;6.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;-3.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="-648.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;5.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="30">
            <position x="312.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="31">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="32">
            <position x="-488.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="33">
            <position x="-440.0" y="1680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="34">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="35">
            <position x="-380.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="36">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="37">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="38">
            <position x="-64.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="39">
            <position x="-544.0" y="1440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="40">
            <position x="-120.0" y="1520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="41">
            <position x="204.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="42">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="43">
            <position x="-276.0" y="1160.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-3.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-1.5)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="44">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-1.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=0.0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="45">
            <position x="260.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>TOTAL_COOLING_CONSUMPTION_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="46">
            <position x="-172.0" y="1400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="47">
            <position x="44.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="48">
            <position x="-596.0" y="1320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-6.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-4.5)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="49">
            <position x="-496.0" y="2000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="50">
            <position x="-328.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;-4.5) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-3.0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="51">
            <position x="-444.0" y="2120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>7.0</coordinate>
            </ndimVector>
        </node>
        <node id="52">
            <position x="-540.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&lt;=-6.0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="53">
            <position x="-336.0" y="1920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="54">
            <position x="-228.0" y="1720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;1.0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="55">
            <position x="-280.0" y="1600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((TOTAL_COOLING_CONSUMPTION_SCALED&gt;0.0) AND (TOTAL_COOLING_CONSUMPTION_SCALED&lt;=1.0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <edge from="32" to="0" />
        <edge from="50" to="0" />
        <edge from="26" to="1" />
        <edge from="45" to="2" />
        <edge from="16" to="2" />
        <edge from="44" to="3" />
        <edge from="19" to="3" />
        <edge from="0" to="4" />
        <edge from="43" to="4" />
        <edge from="3" to="5" />
        <edge from="43" to="5" />
        <edge from="38" to="6" />
        <edge from="11" to="6" />
        <edge from="4" to="7" />
        <edge from="39" to="7" />
        <edge from="42" to="8" />
        <edge from="18" to="8" />
        <edge from="4" to="9" />
        <edge from="5" to="9" />
        <edge from="33" to="10" />
        <edge from="13" to="10" />
        <edge from="47" to="11" />
        <edge from="41" to="11" />
        <edge from="48" to="12" />
        <edge from="25" to="12" />
        <edge from="7" to="13" />
        <edge from="21" to="13" />
        <edge from="1" to="14" />
        <edge from="17" to="15" />
        <edge from="31" to="16" />
        <edge from="23" to="16" />
        <edge from="26" to="17" />
        <edge from="14" to="18" />
        <edge from="29" to="19" />
        <edge from="36" to="19" />
        <edge from="1" to="20" />
        <edge from="17" to="20" />
        <edge from="39" to="21" />
        <edge from="12" to="21" />
        <edge from="33" to="22" />
        <edge from="55" to="22" />
        <edge from="27" to="23" />
        <edge from="18" to="24" />
        <edge from="28" to="25" />
        <edge from="15" to="27" />
        <edge from="52" to="28" />
        <edge from="34" to="29" />
        <edge from="8" to="29" />
        <edge from="45" to="30" />
        <edge from="27" to="31" />
        <edge from="37" to="31" />
        <edge from="35" to="32" />
        <edge from="52" to="32" />
        <edge from="7" to="33" />
        <edge from="9" to="33" />
        <edge from="42" to="34" />
        <edge from="37" to="34" />
        <edge from="8" to="35" />
        <edge from="24" to="35" />
        <edge from="31" to="36" />
        <edge from="34" to="36" />
        <edge from="20" to="37" />
        <edge from="15" to="37" />
        <edge from="3" to="38" />
        <edge from="47" to="38" />
        <edge from="48" to="39" />
        <edge from="0" to="39" />
        <edge from="6" to="40" />
        <edge from="46" to="40" />
        <edge from="30" to="41" />
        <edge from="2" to="41" />
        <edge from="20" to="42" />
        <edge from="14" to="42" />
        <edge from="50" to="43" />
        <edge from="19" to="43" />
        <edge from="36" to="44" />
        <edge from="16" to="44" />
        <edge from="23" to="45" />
        <edge from="38" to="46" />
        <edge from="5" to="46" />
        <edge from="44" to="47" />
        <edge from="2" to="47" />
        <edge from="28" to="48" />
        <edge from="32" to="48" />
        <edge from="10" to="49" />
        <edge from="22" to="49" />
        <edge from="29" to="50" />
        <edge from="35" to="50" />
        <edge from="49" to="51" />
        <edge from="53" to="51" />
        <edge from="24" to="52" />
        <edge from="22" to="53" />
        <edge from="54" to="53" />
        <edge from="40" to="54" />
        <edge from="55" to="54" />
        <edge from="9" to="55" />
        <edge from="46" to="55" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GriSca_Shift_x_RUL">
        <node id="0">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>SHIFT_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="44.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="260.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="148.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-64.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="40.0" y="1440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="96.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="204.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;3.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="256.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>SHIFT_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="-12.0" y="1320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="152.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="312.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;5.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="364.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;6.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;6.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&lt;=0)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;0.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;1) AND (SHIFT_ENCODED&lt;=2)) AND ((RUL_SCALED&gt;0.0) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="30">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;0) AND (SHIFT_ENCODED&lt;=1)) AND ((RUL_SCALED&lt;=0.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>SHIFT_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="31">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((SHIFT_ENCODED&gt;2)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <edge from="30" to="0" />
        <edge from="19" to="1" />
        <edge from="20" to="1" />
        <edge from="12" to="2" />
        <edge from="8" to="3" />
        <edge from="15" to="3" />
        <edge from="6" to="4" />
        <edge from="18" to="4" />
        <edge from="1" to="5" />
        <edge from="31" to="5" />
        <edge from="26" to="6" />
        <edge from="13" to="6" />
        <edge from="3" to="7" />
        <edge from="17" to="7" />
        <edge from="1" to="8" />
        <edge from="10" to="8" />
        <edge from="18" to="9" />
        <edge from="11" to="9" />
        <edge from="20" to="10" />
        <edge from="22" to="10" />
        <edge from="28" to="11" />
        <edge from="16" to="11" />
        <edge from="13" to="12" />
        <edge from="23" to="13" />
        <edge from="25" to="14" />
        <edge from="30" to="14" />
        <edge from="24" to="15" />
        <edge from="10" to="15" />
        <edge from="0" to="16" />
        <edge from="5" to="17" />
        <edge from="8" to="17" />
        <edge from="26" to="18" />
        <edge from="28" to="18" />
        <edge from="4" to="19" />
        <edge from="29" to="19" />
        <edge from="2" to="20" />
        <edge from="29" to="20" />
        <edge from="2" to="22" />
        <edge from="25" to="23" />
        <edge from="22" to="24" />
        <edge from="21" to="25" />
        <edge from="14" to="26" />
        <edge from="23" to="26" />
        <edge from="4" to="27" />
        <edge from="9" to="27" />
        <edge from="14" to="28" />
        <edge from="0" to="28" />
        <edge from="12" to="29" />
        <edge from="6" to="29" />
        <edge from="21" to="30" />
        <edge from="19" to="31" />
        <edge from="27" to="31" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GriSca_Crystalizer_x_RUL">
        <node id="0">
            <position x="-540.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;24</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-4.0" y="440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-332.0" y="1480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-120.0" y="1520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="260.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;4.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-60.0" y="760.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-116.0" y="1080.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-112.0" y="640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="-220.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="40.0" y="1440.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="208.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;3.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="-384.0" y="1360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="96.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-64.0" y="1200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="-176.0" y="1840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="364.0" y="840.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;6.44552</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="-380.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="-216.0" y="400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;6</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="-280.0" y="1600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="-8.0" y="880.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="-488.0" y="1120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="-168.0" y="960.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="-172.0" y="1400.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="-328.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="156.0" y="360.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;2.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="-276.0" y="1160.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="312.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;5.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="28">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;-0.161448</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="29">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_SCALED &gt;1.0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="30">
            <position x="-272.0" y="720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="31">
            <position x="-324.0" y="600.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;12</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="32">
            <position x="-228.0" y="1720.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="33">
            <position x="-436.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;24)) AND ((RUL_SCALED&gt;1.0) AND (RUL_SCALED&lt;=2.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="34">
            <position x="-224.0" y="1280.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="35">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="36">
            <position x="-164.0" y="520.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;-0.161448) AND (RUL_SCALED&lt;=1.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="37">
            <position x="-432.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;18</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="38">
            <position x="152.0" y="800.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="39">
            <position x="-68.0" y="1640.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;18) AND (NUM_CRYSTALLIZER&lt;=24)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="40">
            <position x="148.0" y="1240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="41">
            <position x="204.0" y="920.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="42">
            <position x="-12.0" y="1320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;12) AND (NUM_CRYSTALLIZER&lt;=18)) AND ((RUL_SCALED&gt;5.0) AND (RUL_SCALED&lt;=6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>6.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="43">
            <position x="48.0" y="560.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;2.0) AND (RUL_SCALED&lt;=3.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="44">
            <position x="256.0" y="1040.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;6.44552))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>7.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="45">
            <position x="100.0" y="680.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;1) AND (NUM_CRYSTALLIZER&lt;=6)) AND ((RUL_SCALED&gt;3.0) AND (RUL_SCALED&lt;=4.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>4.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="46">
            <position x="44.0" y="1000.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&gt;6) AND (NUM_CRYSTALLIZER&lt;=12)) AND ((RUL_SCALED&gt;4.0) AND (RUL_SCALED&lt;=5.0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>5.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="47">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((NUM_CRYSTALLIZER&lt;=1)) AND ((RUL_SCALED&lt;=-0.161448))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="37" to="0" />
        <edge from="29" to="1" />
        <edge from="35" to="1" />
        <edge from="11" to="2" />
        <edge from="34" to="2" />
        <edge from="23" to="3" />
        <edge from="42" to="3" />
        <edge from="10" to="4" />
        <edge from="7" to="5" />
        <edge from="43" to="5" />
        <edge from="19" to="6" />
        <edge from="21" to="6" />
        <edge from="1" to="7" />
        <edge from="36" to="7" />
        <edge from="7" to="8" />
        <edge from="30" to="8" />
        <edge from="40" to="9" />
        <edge from="42" to="9" />
        <edge from="25" to="10" />
        <edge from="26" to="11" />
        <edge from="33" to="11" />
        <edge from="41" to="12" />
        <edge from="46" to="12" />
        <edge from="6" to="13" />
        <edge from="46" to="13" />
        <edge from="39" to="14" />
        <edge from="32" to="14" />
        <edge from="27" to="15" />
        <edge from="37" to="16" />
        <edge from="30" to="16" />
        <edge from="22" to="17" />
        <edge from="2" to="18" />
        <edge from="23" to="18" />
        <edge from="5" to="19" />
        <edge from="45" to="19" />
        <edge from="0" to="20" />
        <edge from="16" to="20" />
        <edge from="5" to="21" />
        <edge from="8" to="21" />
        <edge from="47" to="22" />
        <edge from="13" to="23" />
        <edge from="34" to="23" />
        <edge from="8" to="24" />
        <edge from="16" to="24" />
        <edge from="29" to="25" />
        <edge from="21" to="26" />
        <edge from="24" to="26" />
        <edge from="4" to="27" />
        <edge from="47" to="28" />
        <edge from="28" to="29" />
        <edge from="36" to="30" />
        <edge from="31" to="30" />
        <edge from="17" to="31" />
        <edge from="3" to="32" />
        <edge from="18" to="32" />
        <edge from="20" to="33" />
        <edge from="24" to="33" />
        <edge from="6" to="34" />
        <edge from="26" to="34" />
        <edge from="28" to="35" />
        <edge from="22" to="35" />
        <edge from="17" to="36" />
        <edge from="35" to="36" />
        <edge from="31" to="37" />
        <edge from="4" to="38" />
        <edge from="45" to="38" />
        <edge from="3" to="39" />
        <edge from="9" to="39" />
        <edge from="12" to="40" />
        <edge from="44" to="40" />
        <edge from="27" to="41" />
        <edge from="38" to="41" />
        <edge from="12" to="42" />
        <edge from="13" to="42" />
        <edge from="1" to="43" />
        <edge from="25" to="43" />
        <edge from="15" to="44" />
        <edge from="41" to="44" />
        <edge from="43" to="45" />
        <edge from="10" to="45" />
        <edge from="38" to="46" />
        <edge from="19" to="46" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
</conceptualSchema>


import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as blueprints from '@aws-quickstart/eks-blueprints';

import { TeamPlatform, TeamApplication } from '../teams'; 

export default class ClusterConstruct extends Construct {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id);

    const account = props?.env?.account!;
    const region = props?.env?.region!;

    const blueprint = blueprints.EksBlueprint.builder()
    .account(account)
    .region(region)
    .addOns(new blueprints.ClusterAutoScalerAddOn)
    .teams(new TeamPlatform(account), new TeamApplication('burnham',account))
    .build(scope, id+'-stack');
  }
}
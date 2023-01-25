#!/usr/bin/env python3
import os
import aws_cdk as cdk
from personal_account_setup.network_stack import NetworkStack


app = cdk.App()

# creating all the stacks.
NetworkStack(
    app,
    'NetworkStack',
)

app.synth()

# adding tags.
cdk.Tags.of(app).add(
    key='owner',
    value='kiarash@datachef.co'
)

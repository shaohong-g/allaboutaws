# allaboutaws
Useful Aws Tutorials and Documentations

## Prerequisite 
The below examples are experimented in `AWS Academy Leaner Lab`. Hence do **configure** your own IAM roles/users to allow the use of the various AWS resources.

We will be using the following for the creation of AWS services:
- sad
- fds
    - `EC2` -> `Network & Security` -> `Key Pairs` -> `Create key pair`
        - **Name:** cs301-aws-generic
        - **Private key file format:** .pem

## Examples 
<details>
<summary>Public and Private Subnet </summary>

<img src="static/vpc-private-public-subnet.png">  <!-- weight = "" height = "" -->

### Summary
We will be creating a 
- 1 vpc *(IP address of 10.0.0.0/16)* to allow **65534** hosts (256*256 - 2)
- 1 public subnet *(IP address of 10.0.1.0/24)* to allow **254** hosts (256 - 2)
- 1 private subnet *(IP address of 10.0.2.0/24)* to allow **254** hosts (256 - 2)

The key difference between a private and a public subnet is that private subnet associated with a route table that **doesn’t have a route to an internet gateway**.

### Implementation Steps

**NOTE:** You can click **VPC and more** to create a new VPC with 2 public and 2 private subnet configured automatically for you. Click [here](./static/aws-create-vpc-and-more.png) to see the visualisation!


1. Create VPC
    - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Your VPCs` -> `Create VPC`
        - **Name:** vpc-demo
        - **IPv4 CIDR:** 10.0.0.0/16
2. Create Subnet for both private and public
    - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Subnets` -> `Create subnet`
        - **VPC ID:** <select your VPC from (1)> 
        - **Subnet name:** subnet-public-1, subnet-private-1
        - **Availability Zone:** us-east-1a , us-east-1b *(you can allow AWS to choose for you but I assign manually for better control of resources later on)*
        - **IPv4 CIDR block:** 10.0.1.0/24 , 10.0.2.0/24 respectively
        - CLICK `add new subnet` to add more
3. Create a new Internet gateways
    - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Internet gateways` -> `Create internet gateway`
        - **Name tag:** demo-internet-gateway
    - Click on your gateway, from `Actions` -> `Attach to VPC` 
        - **Available VPCs**: <select your VPC from (1)> 
4. Create Route tables for your private and public subnets
    - Do note that a default route table is already attached during the creation of VPC. In this case we will be using the **default route table for the private subnet** since it is not routed to any internet gateway.
        <img src="static/aws-default-route-table.png">
    - Change the name of the default route table for the private subnet
        - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Route tables`
        - Find the default route table that is under your vpc and hover your mouse-tip to the `-` under the `Name` column.
            - **Edit Name:**: rt-private-1
    - Create route table for public subnet
        - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Route tables` -> `Create route table`
            - **Edit Name:**: rt-public
            - **VPC:** <select your VPC from (1)> 
        - Once created, click on `Edit Routes` and `Add route`
            - **Destination:** 0.0.0.0/0
            - **Target:** Click `Internet Gateway` and you will see the gateway that you have attached in (3)
5. Change the route table for your public subnet *(private subnet should already be attached to the default route table which you renamed at (4))*
    - `VPC (service)` -> `Virtual private cloud (left navigation menu)` -> `Subnets`
    - Click on your public subnet *(subnet-public-1)*
    - Under `Route table`, click `Edit route association` and change the route table ID
        - **Route table ID:**: rt-public
6. YAY! you have successfully setup a private and a public subnet under your own VPC! You can visualise the resource map by clicking on your `VPC`. From the image below, you can see that the two different subnets are associated with different route table. Only the public subnet can access the internet gateway.
    <img src="static/aws-vpc-setup-demo.png">



</details>



## Resources and References
- [AWS - Creation of public and private subnet](https://www.1cloudhub.com/aws-vpc-101-creation-of-public-subnet-and-private-subnet-in-vpc-and-test-connectivity/)
- [Subnet Calculator](https://www.davidc.net/sites/default/subnets/subnets.html)
- [Youtube - Subnet Mask Explained](https://www.youtube.com/watch?v=s_Ntt6eTn94)


Connect-AzAccount

$context = Get-AzSubscription -SubscriptionName 'AZ-900'
Set-AzContext $context

$rgName="rg001"
$location="australiaeast"
$sbName="sbiwclientapp001"
$topicName= "appTopic"
#$miName="mi-app-2-blob"
#$scope = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.Storage/storageAccounts/$staName"
New-AzResourceGroup -Name $rgName -Location $location


$serviceBus = New-AzServiceBusNamespaceV2 -Name $sbName -ResourceGroupName $rgName -Location $location -SkuName Standard -Tag @{env='dev'}

New-AzServiceBusTopic -Name $topicName  -ResourceGroupName $rgName -NamespaceName $sbName

New-AzServiceBusSubscription -Name 'sub1' -ResourceGroupName $rgName -NamespaceName $sbName -TopicName $topicName `
-DefaultMessageTimeToLive (New-TimeSpan -Minutes 5)

New-AzServiceBusSubscription -Name 'sub2' -ResourceGroupName $rgName -NamespaceName $sbName -TopicName $topicName `
-DefaultMessageTimeToLive (New-TimeSpan -Minutes 5) -Status 'Active'


New-AzServiceBusSubscription -Name 'subEngineering' -ResourceGroupName $rgName -NamespaceName $sbName -TopicName $topicName `
-DefaultMessageTimeToLive (New-TimeSpan -Minutes 5)


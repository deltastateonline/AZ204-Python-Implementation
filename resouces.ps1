Connect-AzAccount

$context = Get-AzSubscription -SubscriptionName 'AZ-900'
Set-AzContext $context

#$subId = $context.Id

$rgName="rg001"
$location="australiaeast"
$staName="staiwclientapp002"
#$miName="mi-app-2-blob"
#$scope = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.Storage/storageAccounts/$staName"
New-AzResourceGroup -Name $rgName -Location $location


$storageAccount = New-AzStorageAccount -ResourceGroupName $rgName `
  -Name $staName `
  -Location $location `
  -SkuName 'Standard_LRS' `
  -Kind 'StorageV2' `
  -AllowBlobPublicAccess $false

$stactx = New-AzStorageContext -StorageAccountName $staName -UseConnectedAccount

New-AzStorageContainer -Name 'photos' -Context $stactx
New-AzStorageQueue -Name 'queue01' -Context $stactx


Get-AzResource -ResourceGroupName $rgName -Name $staName


New-AzRoleAssignment -SignInName 'omokhoa@integrationworksau.onmicrosoft.com' -RoleDefinitionName "Storage Queue Data Contributor" -Scope $storageAccount.Id
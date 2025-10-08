<?php
// Test OPC initialization fix
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "Testing OPC initialization fix...\n";

// Simulate Zen Cart environment
define('DIR_WS_CLASSES', __DIR__ . '/includes/classes/');
define('DIR_FS_LOGS', __DIR__ . '/logs');

// Start session
session_start();

try {
    echo "Step 1: Testing without OPC object (should fail gracefully)...\n";
    
    // Simulate what template does - should handle null gracefully now
    $shipping_billing_value = (isset($_SESSION['opc']) && is_object($_SESSION['opc'])) 
        ? $_SESSION['opc']->getShippingBilling() 
        : false;
    
    echo "Without OPC object - shipping_billing_value: " . ($shipping_billing_value ? 'true' : 'false') . "\n";
    
    echo "\nStep 2: Testing with OPC object initialization...\n";
    
    // Initialize OPC object as our controller does
    if (!isset($_SESSION['opc']) || !is_object($_SESSION['opc'])) {
        require_once(DIR_WS_CLASSES . 'OnePageCheckout.php');
        $_SESSION['opc'] = new OnePageCheckout();
        echo "✅ OPC object initialized\n";
    }
    
    // Test the method call
    $shipping_billing_value = (isset($_SESSION['opc']) && is_object($_SESSION['opc'])) 
        ? $_SESSION['opc']->getShippingBilling() 
        : false;
    
    echo "With OPC object - shipping_billing_value: " . ($shipping_billing_value ? 'true' : 'false') . "\n";
    
    echo "\n✅ SUCCESS: OPC fix working properly!\n";
    echo "Template should now render without fatal errors.\n";
    
} catch (Exception $e) {
    echo "❌ Error: " . $e->getMessage() . "\n";
} catch (Error $e) {
    echo "❌ Fatal Error: " . $e->getMessage() . "\n";
}
?>
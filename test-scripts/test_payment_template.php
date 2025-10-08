<?php
// Direct test of payment template processing
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Simulate basic Zen Cart environment
define('DIR_FS_LOGS', __DIR__ . '/logs');
define('DIR_WS_MODULES', __DIR__ . '/includes/modules/');

// Simple test to see if template can be included
echo "Testing payment template inclusion...\n";

try {
    ob_start();
    
    // Mock the required variables that template expects
    $payment_modules = new stdClass();
    $payment_modules->javascript_validation = function() {
        return '// Mock JS validation';
    };
    
    $messageStack = new stdClass(); 
    $messageStack->size = function($type) {
        return 0; // No messages
    };
    
    echo "About to include template...\n";
    include('/home/user1/shawndev1/ASAPWebNew/includes/templates/goodwin/templates/views/opc_checkout_payment.php');
    echo "Template inclusion completed\n";
    
    $output = ob_get_clean();
    echo "Output length: " . strlen($output) . "\n";
    
} catch (Exception $e) {
    echo "Exception caught: " . $e->getMessage() . "\n";
} catch (Error $e) {
    echo "Error caught: " . $e->getMessage() . "\n";
}
?>
var dashAgGridComponentFunctions = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dashAgGridComponentFunctions.Button = function (props) {
    const {setData, buttonName, buttonClassName, iconClassName, disabled} = props;

    function onClick() {
        setData();
    }

    return React.createElement(
        "button",
        {
            onClick,
            disabled,
            className: buttonClassName + " dash-ag-grid-table-button"
        },
        buttonName, " ", React.createElement("i", {className: iconClassName}, "")
    );

};

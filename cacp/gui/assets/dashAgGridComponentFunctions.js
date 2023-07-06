var dashAgGridComponentFunctions = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dashAgGridComponentFunctions.Button = function (props) {
    const {setData, buttonName, buttonClassName, iconClassName} = props;

    function onClick() {
        setData();
    }

    return React.createElement(
        "button",
        {
            onClick: onClick,
            className: buttonClassName
        },
        buttonName, " ", React.createElement("i", {className: iconClassName}, "")
    );

};
